# core-decrypt
Tool for recovering Bitcoin Core wallet passwords. Requires an OpenCL device.

## Attribution
This is a Windows-compatible fork of the original [core-decrypt](https://github.com/brichard19/core-decrypt/tree/master) by brichard19. The main improvement in this version is that `walletinfo.py` has been updated to work on Windows without requiring the deprecated `bsddb.db` library or its problematic replacements (`bsddb3`/`berkeleydb`) that often fail to install on Windows systems.

### Changes from original:
- Replaced Berkeley DB dependency with pure Python implementation
- Fixed Windows compatibility issues
- Maintained full compatibility with the original encrypted key format
- **NEW**: Added comprehensive progress reporting with real-time ETA calculations
- **NEW**: Enhanced verbose output showing processing speed and time estimates
- **NEW**: Pre-flight benchmarking for high iteration count detection
- **NEW**: User-configurable progress update intervals via `--eta-interval`

### Features:
- **Progress Tracking**: Real-time display of passwords processed, percentage complete, and estimated time remaining
- **Speed Monitoring**: Shows processing speed in passwords per second
- **Batch Progress**: Detailed progress reporting for each batch of passwords tested
- **Enhanced Debugging**: Verbose output for troubleshooting dictionary and encrypted key issues

### Known Issues:
- The `walletinfo.py` script may display a warning about "unexpected Bitcoin Core key derivation method" due to the manual parsing approach. This warning can be safely ignored as the encrypted key extraction still works correctly.

### Note: Please test against some of the sample wallets to verify the program works properly. Each vendor has a different OpenCL implementation, and I am unable to test all of them

## Building

### Prerequisites
- MSYS2 with MinGW 64-bit environment
- OpenCL headers and libraries
- C++ compiler with C++11 support

### Windows Build Instructions

1. Install MSYS2 from https://www.msys2.org/
2. Open MSYS2 MinGW 64-bit terminal
3. Install required packages:
   ```bash
   pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-opencl-headers mingw-w64-x86_64-opencl-icd-loader
   ```
4. Navigate to the project directory and build:
   ```bash
   cd /c/path/to/core-decrypt/src
   g++ -std=c++11 -O3 -o ../core-decrypt.exe *.cpp embedcl/*.cpp -lOpenCL
   ```
5. Copy required runtime DLLs to the output directory:
   ```bash
   cp /mingw64/bin/libgcc_s_seh-1.dll /mingw64/bin/libstdc++-6.dll ../
   ```

### Alternative Build with Make
You can also use the provided Makefile (Linux-oriented but works in MSYS2):
```bash
make
```

### Windows Batch Script
For convenience, you can use the provided `build.bat` script from Windows Command Prompt or PowerShell:
```cmd
build.bat
```
This script automatically launches the MSYS2 environment and runs the Makefile.

### Running the Program
The executable requires the MinGW runtime DLLs (`libgcc_s_seh-1.dll` and `libstdc++-6.dll`) to be in the same directory or in your PATH.

## Quick Start Guide

1. **Prepare your wallet file**: Place your Bitcoin Core `wallet.dat` file in the project directory
2. **Extract the encrypted key**: Run `python walletinfo.py wallet.dat` to get the encrypted master key
3. **Create your wordlist**: Create a file called `wordlist.txt` with potential passwords (one per line)
4. **Run the attack**: Use the command below with your encrypted key and wordlist

## Usage

```
core-decrypt [OPTIONS] [ENCRYPTED_MASTER_KEY] [WORD FILES ..]

--list-devices          List devices then exit
--device NUM            Use device NUM
--start NUM             Specify where in the password space to start
--eta-interval SECONDS  Progress update interval in seconds (default: 30)
```

### Basic Example
```bash
# Extract encrypted key from wallet
python walletinfo.py wallet.dat

# Run password attack with custom wordlist
core-decrypt.exe --device 0 [ENCRYPTED_KEY_FROM_ABOVE] wordlist.txt
```

### Creating Your Wordlist

Create a text file called `wordlist.txt` (or any name you prefer) with potential passwords, one per line:

```
password123
mybirthday1990
familyname2020
secretword
combination123
```

The program supports multiple wordlist files for complex combinations. For example:
```bash
# Try combinations of words from multiple files
core-decrypt.exe [ENCRYPTED_KEY] words1.txt words2.txt numbers.txt
```

This will test all combinations like: `[word1][word2][number]`

### Using Sample Wallets for Testing

The project includes sample wallets in `sample_wallets/` directory. The filename indicates the password:
- `1234.dat` → password is "1234"  
- `football.dat` → password is "football"
- `hunter2.dat` → password is "hunter2"

Test with a sample wallet:
```bash
python walletinfo.py sample_wallets/1234.dat
core-decrypt.exe --device 0 [ENCRYPTED_KEY] word_lists/4_digit_numbers.txt
```

### Progress Reporting Options

The `--eta-interval` option controls how frequently progress updates are displayed during long-running hash computations:

- **Default (30 seconds)**: Suitable for most use cases, provides regular updates without flooding the console
- **Shorter intervals (5-15 seconds)**: Better for interactive monitoring of shorter jobs
- **Longer intervals (60+ seconds)**: Reduces console output for very long-running jobs

Example with custom progress interval:
```
core-decrypt --eta-interval 10 --device 0 [ENCRYPTED_KEY] wordlist.txt
```

### Reading the encrypted master key

Run the `walletinfo.py` script on the wallet file. The output contains the encrypted master key, number of iterations, and salt.

```
# python walletinfo.py wallet.dat
walletinfo.py: warning: unexpected Bitcoin Core key derivation method  4110353185
ec01bd09d2befa62ec34609fa2e19316063a9a688aef03494ab9a4d8ba67e24c414609b1ce5abb850002ecc0
```

Note: The warning message can be safely ignored. The important output is the hexadecimal string on the second line.

### Recovering the password

Pass the output to the `core-decrypt` program

```
# core-decrypt.exe ec01bd09d2befa62ec34609fa2e19316063a9a688aef03494ab9a4d8ba67e24c414609b1ce5abb850002ecc0  dictionary.txt
```

The program will display real-time progress information:
```
Selected gfx1036
Building kernel... Done
Finding optimal kernel size for gfx1036
Running...
Total passwords to check: 5
Iterations per password: 2684289640
High iteration count detected. Running quick benchmark...
Benchmark results:
Time per iteration: 0.008 ms
Estimated time per password: 05:48:57
Estimated total time: 1:05:04:47
WARNING: This will take a very long time!
Consider using a smaller wordlist or lower iteration count for testing.
Progress updates will be shown every 30 seconds.
Press Ctrl+C to cancel if this is too long.
Starting full attack...
Testing passwords 0 to 5 of 5
Starting hash computation with 2684289 iterations...
Passwords 0-4/5 - Hash progress: 1000/2684289 (0.0%) Overall: 0.01% ETA: 05:47:32
```

### Progress Output Explained

- **Benchmark**: For high iteration counts (>1M), shows estimated runtime before starting
- **Hash Progress**: Shows current iteration within the hashing phase for each password
- **Overall Progress**: Percentage complete across all passwords in the dictionary  
- **ETA**: Estimated time remaining based on current processing speed
- **Speed**: Processing rate in passwords per second (for completed batches)

For smaller dictionaries, you'll see simpler progress:
```
Progress: 1024/15 (100.00%) Complete!
Total time: 00:00:05
```

The dictionaries contain one password per line. The program will try each password until it finds the correct one or exhausts the list.




More complex passwords


Multiple dictionaries can be combined together to form complex password combinations


For example, if you know the password consists of two words and a number, you might use 

```
# core-decrypt <encrypted key> words1.txt words2.txt 0_to_9.txt
```

This will try all combinations of passwords in the form,

```
[word from words1.txt][word from words2.txt][number]
```

### Sample wallets
There are some sample wallets for testing. The file name of the wallet is the password.

TODO List:

* Multi-GPU support
* Password rules
* Allow more performance tuning by user
* Better word lists

## Recent Updates

### Version 2.0 - Enhanced Progress Reporting (2025)
- **NEW**: Added `--eta-interval` command-line option to control progress update frequency
- **NEW**: Real-time progress tracking with percentage completion during hash computation
- **NEW**: Pre-flight benchmark for high iteration counts with runtime warnings
- **NEW**: Enhanced ETA calculations showing estimated time remaining
- **NEW**: Improved speed monitoring displaying passwords per second
- **NEW**: Detailed batch progress reporting for better user feedback
- **NEW**: Verbose debugging output for troubleshooting dictionary and encrypted key issues
- **IMPROVED**: Optimized progress display logic for both small and large dictionaries
- **IMPROVED**: Better handling of very long-running jobs with time-based progress updates

### Key Features:
- **Smart Benchmarking**: Automatically detects high iteration counts and runs quick benchmarks
- **Adaptive Progress**: Different progress reporting strategies for small vs large dictionaries  
- **User Control**: Configurable update intervals via `--eta-interval` parameter
- **Time Warnings**: Alerts users to potentially very long-running jobs before starting

### Build Environment
- Tested and verified with MSYS2 MinGW 64-bit
- Compatible with modern OpenCL implementations
- Streamlined build process with clear dependency requirements
