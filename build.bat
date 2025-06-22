@echo off
echo Building core-decrypt with ETA support...
echo NOTE: This script launches MSYS2 MinGW 64-bit environment to build
echo If MSYS2 is not installed, please follow the manual build instructions in README.md
echo.

REM Check if MSYS2 is installed
if not exist "C:\msys64\msys2_shell.cmd" (
    echo Error: MSYS2 not found at C:\msys64\
    echo Please install MSYS2 or use the manual build instructions in README.md
    exit /b 1
)

echo Starting MSYS2 MinGW 64-bit build environment...
C:\msys64\msys2_shell.cmd -mingw64 -defterm -no-start -c "cd '%~dp0src' && make"

if %errorlevel% neq 0 (
    echo Build failed. Please check the error messages above.
    echo You can also try building manually using the instructions in README.md
    exit /b 1
)

echo Build complete! Executable created as core-decrypt.exe
