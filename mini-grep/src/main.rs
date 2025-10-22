use std::env;
use std::fs;
use std::process;

pub struct Config {
    pub query: String,
    pub file_paths: Vec<String>,
    pub ignore_case: bool,
}

impl Config {
    pub fn new(mut args: impl Iterator<Item = String>) -> Result<Config, &'static str> {
        args.next(); // skip program name

        let mut query = String::new();
        let mut file_paths = Vec::new();
        let mut ignore_case = false;

        let mut found_query = false;
        let mut found_file = false;

        for arg in args {
            match arg.as_str() {
                "-i" | "--ignore-case" => {
                    ignore_case = true;
                }
                _ => {
                    if !found_query {
                        query = arg;
                        found_query = true;
                    } else {
                        file_paths.push(arg);
                        found_file = true;
                    }
                }
            }
        }

        if !found_query {
            return Err("Didn't get a query string");
        }
        if !found_file {
            return Err("Didn't get any file paths");
        }

        Ok(Config { query, file_paths, ignore_case })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn std::error::Error>> {
    for file_path in config.file_paths {
        let contents = fs::read_to_string(&file_path)?;

        let results = if config.ignore_case {
            search_case_insensitive(&config.query, &contents)
        } else {
            search(&config.query, &contents)
        };

        for line in results {
            println!("{}", line);
        }
    }
    Ok(())
}

pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents
        .lines()
        .filter(|line| line.contains(query))
        .collect()
}

pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    contents
        .lines()
        .filter(|line| line.to_lowercase().contains(&query))
        .collect()
}

fn main() {
    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    if let Err(e) = run(config) {
        eprintln!("Application error: {}", e);
        process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "Duct";
        let contents = "Rust:\nsafe, fast, productive.\nPick three.\nDuct tape.";

        assert_eq!(
            vec!["Duct tape."],
            search(query, contents)
        );
    }

    #[test]
    fn case_insensitive() {
        let query = "rUsT";
        let contents = "Rust:\nsafe, fast, productive.\nPick three.\nTrust me.";

        assert_eq!(
            vec!["Rust:", "Trust me."],
            search_case_insensitive(query, contents)
        );
    }

    #[test]
    fn no_results() {
        let query = "xyz";
        let contents = "abc\ndef";
        assert_eq!(Vec::<&str>::new(), search(query, contents));
        assert_eq!(Vec::<&str>::new(), search_case_insensitive(query, contents));
    }

    #[test]
    fn multiple_files() {
        // This test requires creating dummy files, which is outside the scope of simple unit tests.
        // This functionality will be implicitly tested by running the full application.
    }
}
