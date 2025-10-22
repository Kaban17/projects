
# SHA-256 Hash Finder

A simple, multi-threaded Rust utility for finding numbers whose SHA-256 hash (in hexadecimal representation) ends with a specified number of zeros.

## Description

This program iterates through numbers (starting from 1), calculates their SHA-256 hash, and checks if it meets the required condition (ending in $N$ zeros). The search is performed in parallel using a configurable number of threads for maximum performance.

## Building

You will need [Rust and Cargo](https://www.rust-lang.org/tools/install) to build the project.

1.  Clone the repository:

    ```sh
    git clone <YOUR_REPOSITORY_URL>
    cd hash_finder
    ```

2.  Build the project in **release** (optimized) mode:

    ```sh
    cargo build --release
    ```

3.  The executable will be located at `target/release/hash_finder`.

## Usage

The program is run from the command line and requires two arguments.

```sh
./target/release/hash_finder [OPTIONS]
```

### Command-Line Options

  * `-N, --zeros <ZEROS>`: **(Required)** The number of trailing zeros required in the hash.
  * `-F, --results <RESULTS>`: **(Required)** The number of results to find before the program stops.
  * `-t, --threads <THREADS>`: **(Optional)** The number of threads to use for the search. By default, the program uses all available logical CPU cores.

## Example

Find **2** numbers whose SHA-256 hash ends in **3** zeros, using **4** threads:

```sh
./target/release/hash_finder -N 3 -F 2 -t 4
```

### Example Output

The output will be in the format `NUMBER, "HASH"`. The order of the output is not guaranteed due to parallel processing.

```
4163, "95d4362bd3cd4315d0bbe38dfa5d7fb8f0aed5f1a31d98d510907279194e3000"
11848, "cb58074fd7620cd0ff471922fd9df8812f29f302904b15e389fc14570a66f000"
```

## Testing

To run the built-in unit tests, execute:

```sh
cargo test
```
