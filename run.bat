@echo off
REM otp generator batch script
REM Usage: run.bat [input_file] [output_name]

set INPUT_FILE=input\cygnetpluse_otp_map.txt
set OUTPUT_NAME=cygnetpluse_otp_distributor.sv

if "%INPUT_FILE%"=="" (
    echo ========================================
    echo   OTP Distributor Generator
    echo ========================================
    echo.
    echo Usage: run.bat [input_file] [output_name]
    echo.
    echo Examples:
    echo   run.bat input\cygnetpluse_otp_map.txt cygnetpluse_otp_distributor.sv
    echo   run.bat input\my_signal.csv my_distributor.sv
    echo.
    echo Available input files:
    dir /b input\*.txt input\*.csv 2>nul
    echo.
    pause
    exit /b 1
)

if "%OUTPUT_NAME%"=="" (
    set OUTPUT_NAME=distributor.sv
)

echo.
echo [INFO] Generating OTP distributor...  
echo [INFO] Input:  %INPUT_FILE%
echo [INFO] Output: generated\%OUTPUT_NAME%
echo.

python src\dynamic_signal_parser.py -i %INPUT_FILE% -o %OUTPUT_NAME%

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Generation completed!
    echo [OUTPUT] generated\%OUTPUT_NAME%
    echo [EXCEL]  generated\*_byte_table_*.xlsx
) else (
    echo.
    echo [ERROR] Generation failed!
    pause
    exit /b 1
)

echo.
pause
