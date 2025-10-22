# mini-grep

`mini-grep` is a command-line tool written in Rust that functions like the classic `grep` command. It allows you to search for a specified query string within one or more files. It supports both case-sensitive and case-insensitive searches.

## Table of Contents

- [Features](#features)
- [Building](#building)
- [Usage](#usage)
- [Examples](#examples)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- Search for a query string in multiple files.
- Case-sensitive search by default.
- Case-insensitive search using the `-i` or `--ignore-case` flag.
- Provides clear error messages for incorrect usage.

## Building

To build `mini-grep`, you need to have Rust and Cargo installed. If you don't have them, you can install them by following the instructions on the [official Rust website](https://www.rust-lang.org/tools/install).

Once Rust and Cargo are installed, navigate to the root directory of the `mini-grep` project and run the following command:

```bash
cargo build
```

This will compile the project and create an executable in the `target/debug/` directory.

## Usage

The basic usage of `mini-grep` is as follows:

```bash
mini-grep <query> <file_path1> [file_path2 ...] [-i | --ignore-case]
```

- `<query>`: The string you want to search for.
- `<file_path1> [file_path2 ...]`: One or more paths to the files you want to search within.
- `-i` or `--ignore-case`: (Optional) Flag to perform a case-insensitive search.

## Examples

1. **Case-sensitive search for "hello" in `file.txt`:**

   ```bash
   ./target/debug/mini-grep hello file.txt
   ```

2. **Case-insensitive search for "rust" in `main.rs` and `lib.rs`:**

   ```bash
   ./target/debug/mini-grep -i rust src/main.rs src/lib.rs
   ```

   Or:

   ```bash
   ./target/debug/mini-grep --ignore-case rust src/main.rs src/lib.rs
   ```

3. **Searching for a phrase (remember to quote it):**

   ```bash
   ./target/debug/mini-grep "Duct tape" poem.txt
   ```

## Running Tests

To run the tests for `mini-grep`, navigate to the root directory of the project and execute the following command:

```bash
cargo test
```

