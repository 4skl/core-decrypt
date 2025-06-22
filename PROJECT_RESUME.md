# Project Resume: core-decrypt OpenCL Password Recovery Tool

## Current Status: NVIDIA OpenCL Kernel Fix Applied - NEEDS TESTING

### Project Overview
Windows-compatible Bitcoin Core wallet password recovery tool using OpenCL acceleration. Fork of brichard19's original core-decrypt with Windows compatibility improvements and enhanced progress reporting.

### Recent Issue Resolved
**PROBLEM**: OpenCL kernel compilation failure on NVIDIA GeForce RTX 3050 Ti Laptop GPU
```
Error: Failed to build program executable! error code -11
<kernel>:282:24: error: passing 'const __generic unsigned int *' to parameter of type 'const unsigned int *' changes address space of pointer
    aes_256_key_expand(key, subkeys);
                       ^~~
```

**SOLUTION APPLIED**: Fixed address space mismatch in `src/core-decrypt.cl` line 221
- Changed: `void aes_256_key_expand(__private const unsigned int *key, unsigned int *subkeys)`
- To: `void aes_256_key_expand(__private const unsigned int *key, __private unsigned int *subkeys)`

### What Needs To Be Done Next

1. **REBUILD THE PROJECT** (Critical - Required Before Testing)
   ```bash
   # From MSYS2 MinGW 64-bit terminal:
   cd /c/Users/medio/Desktop/Prog/core-decrypt/src
   make clean && make
   
   # OR use the build script from PowerShell:
   cd "c:\Users\medio\Desktop\Prog\core-decrypt"
   .\build.bat
   ```

2. **TEST THE FIX**
   ```bash
   # Test device detection (should not show OpenCL compilation error):
   .\core-decrypt.exe --list-devices
   
   # Test with sample wallet:
   python walletinfo.py sample_wallets/1234.dat
   .\core-decrypt.exe --device 0 [ENCRYPTED_KEY_FROM_ABOVE] word_lists/4_digit_numbers.txt
   ```

3. **VERIFY NVIDIA COMPATIBILITY**
   - Confirm kernel builds without errors
   - Verify password cracking works on NVIDIA hardware
   - Test ETA/progress reporting functionality

### Project Structure
```
core-decrypt/
├── src/
│   ├── core-decrypt.cl          # OpenCL kernel (FIXED - address space)
│   ├── hash_opencl.cpp          # ETA/progress reporting logic
│   ├── main.cpp                 # Command-line argument parsing
│   ├── core-decrypt.h           # Function signatures
│   └── Makefile                 # Build configuration
├── sample_wallets/              # Test wallets (password = filename)
├── word_lists/                  # Project wordlists
├── build.bat                    # Windows build script
├── walletinfo.py               # Windows-compatible wallet parser
└── README.md                   # Comprehensive documentation
```

### Key Features Implemented (Version 2.0)
- **ETA/Progress Reporting**: Real-time progress with configurable update intervals (`--eta-interval`)
- **Pre-flight Benchmarking**: Warns about long-running jobs before starting
- **Enhanced Debugging**: Verbose output for troubleshooting
- **Windows Compatibility**: Pure Python wallet parsing, no Berkeley DB dependency
- **MSYS2 Build Support**: Streamlined build process with clear instructions

### Build Environment
- **Platform**: Windows with MSYS2 MinGW 64-bit
- **Dependencies**: OpenCL headers/libraries, GCC with C++11 support
- **Runtime**: Requires `libgcc_s_seh-1.dll` and `libstdc++-6.dll`

### Recent Changes Made
1. **OpenCL Kernel Fix**: Added `__private` address space qualifier to `subkeys` parameter
2. **Progress System**: Comprehensive ETA calculations and batch reporting
3. **Build System**: Updated Makefile and build.bat for Windows
4. **Documentation**: Overhauled README with clear build/usage instructions
5. **Git Cleanup**: Updated .gitignore to exclude user files, keep samples

### User's Environment
- **OS**: Windows with PowerShell
- **GPU**: NVIDIA GeForce RTX 3050 Ti Laptop GPU
- **Working Directory**: `c:\Users\medio\Desktop\Prog\core-decrypt`
- **Build Tool**: MSYS2 MinGW 64-bit environment

### Testing Commands Ready
```bash
# Device listing
.\core-decrypt.exe --list-devices

# Sample wallet test (password: "1234")
python walletinfo.py sample_wallets/1234.dat
.\core-decrypt.exe --device 0 [KEY] word_lists/4_digit_numbers.txt

# Custom wordlist test
.\core-decrypt.exe --eta-interval 10 --device 0 [KEY] wordlist.txt
```

### Expected Results After Fix
- Device detection should show: `ID: 0, Name: gfx1036` (NVIDIA card)
- No OpenCL compilation errors
- Kernel should build successfully: "Building kernel... Done"
- Progress reporting should work with configurable intervals
- Sample wallet "1234" should be cracked quickly with 4_digit_numbers.txt

### Files Modified in This Session
- `src/core-decrypt.cl`: Line 221 - Added `__private` qualifier to fix NVIDIA compatibility
- Previous sessions added comprehensive ETA/progress system

### Critical Next Step
**The fix has been applied but the project MUST be recompiled before testing.** The current executable may still have the old kernel code embedded. Use `build.bat` or manual MSYS2 compilation to rebuild with the fixed kernel.
