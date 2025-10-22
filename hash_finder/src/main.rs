use clap::Parser;
use sha2::{Digest, Sha256};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::thread;

/// SHA-256 Hash Finder - finds numbers whose hash ends with N zeros
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of trailing zeros required in the hash
    #[arg(short = 'N', long)]
    zeros: usize,

    /// Number of results to find before stopping
    #[arg(short = 'F', long)]
    results: usize,

    /// Number of threads to use (default: number of CPU cores)
    #[arg(short = 't', long)]
    threads: Option<usize>,
}

fn main() {
    let args = Args::parse();

    // Validate inputs
    if args.zeros == 0 {
        eprintln!("Error: N (zeros) must be greater than 0");
        std::process::exit(1);
    }

    if args.results == 0 {
        eprintln!("Error: F (results) must be greater than 0");
        std::process::exit(1);
    }

    // Determine number of threads
    let num_threads = args.threads.unwrap_or_else(|| num_cpus::get());

    // Shared state
    let counter = Arc::new(AtomicU64::new(1));
    let found_count = Arc::new(AtomicU64::new(0));
    let should_stop = Arc::new(AtomicBool::new(false));

    // Spawn worker threads
    let mut handles = vec![];

    for _ in 0..num_threads {
        let counter = Arc::clone(&counter);
        let found_count = Arc::clone(&found_count);
        let should_stop = Arc::clone(&should_stop);
        let target_results = args.results;
        let required_zeros = args.zeros;

        let handle = thread::spawn(move || {
            loop {
                // Check if we should stop
                if should_stop.load(Ordering::Relaxed) {
                    break;
                }

                // Get next number to check
                let num = counter.fetch_add(1, Ordering::Relaxed);

                // Calculate hash
                let hash = calculate_sha256(num);

                // Check if hash ends with required zeros
                if ends_with_n_zeros(&hash, required_zeros) {
                    let current_found = found_count.fetch_add(1, Ordering::SeqCst);

                    // Print result (with lock to avoid interleaved output)
                    println!("{}, \"{}\"", num, hash);

                    // Check if we've found enough results
                    if current_found + 1 >= target_results as u64 {
                        should_stop.store(true, Ordering::Relaxed);
                        break;
                    }
                }
            }
        });

        handles.push(handle);
    }

    // Wait for all threads to complete
    for handle in handles {
        handle.join().unwrap();
    }
}

/// Calculate SHA-256 hash of a number
fn calculate_sha256(num: u64) -> String {
    let mut hasher = Sha256::new();
    hasher.update(num.to_string().as_bytes());
    let result = hasher.finalize();
    format!("{:x}", result)
}

/// Check if a hash string ends with N zeros
fn ends_with_n_zeros(hash: &str, n: usize) -> bool {
    if hash.len() < n {
        return false;
    }

    hash.chars().rev().take(n).all(|c| c == '0')
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_sha256() {
        // Test known hash values
        let hash1 = calculate_sha256(1);
        assert_eq!(hash1.len(), 64); // SHA-256 produces 64 hex characters

        // Hash should be deterministic
        let hash2 = calculate_sha256(1);
        assert_eq!(hash1, hash2);
    }

    #[test]
    fn test_ends_with_n_zeros() {
        assert!(ends_with_n_zeros("abc000", 3));
        assert!(ends_with_n_zeros("abc0000", 4));
        assert!(!ends_with_n_zeros("abc000", 4));
        assert!(ends_with_n_zeros("abc100", 2));
        assert!(ends_with_n_zeros("0000", 4));
        assert!(!ends_with_n_zeros("abc", 5));
    }

    #[test]
    fn test_ends_with_one_zero() {
        assert!(ends_with_n_zeros("abc0", 1));
        assert!(!ends_with_n_zeros("abc1", 1));
    }

    #[test]
    fn test_known_hashes_with_zeros() {
        // Number 4163 should end with 3 zeros
        let hash = calculate_sha256(4163);
        assert!(ends_with_n_zeros(&hash, 3));

        // Number 11848 should end with 3 zeros
        let hash = calculate_sha256(11848);
        assert!(ends_with_n_zeros(&hash, 3));
    }

    #[test]
    fn test_empty_string() {
        assert!(ends_with_n_zeros("", 0));
        assert!(!ends_with_n_zeros("", 1));
    }
}
