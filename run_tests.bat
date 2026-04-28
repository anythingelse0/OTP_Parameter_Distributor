@echo off
chcp 65001 >nul 2>&1

:: OTP Distributor Generator - Regression Test Script
:: Usage: run_tests.bat          - Run tests with coverage
::        run_tests.bat verbose  - Run tests with verbose output
::        run_tests.bat html     - Generate HTML coverage report

echo.
echo ============================================================
echo           OTP Distributor - Regression Tests
echo ============================================================
echo.

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    exit /b 1
)

:: Check for coverage module
python -c "import coverage" >nul 2>&1
if errorlevel 1 (
    echo Installing coverage module...
    pip install coverage -q
)

:: Check for openpyxl module
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installing openpyxl module...
    pip install openpyxl -q
)

:: Run tests based on argument
if /i "%~1"=="verbose" goto verbose
if /i "%~1"=="html" goto html

:: Default: Normal test run with coverage
echo [INFO] Running regression tests with coverage...
echo.
python -m coverage run -m unittest discover tests
if errorlevel 1 (
    echo.
    echo [ERROR] Tests failed!
    exit /b 1
)
echo.
echo [INFO] Generating coverage report...
python -m coverage report --include=src/dynamic_signal_parser.py
goto done

:verbose
echo [INFO] Running regression tests (verbose mode)...
echo.
python -m coverage run -m unittest discover tests -v
if errorlevel 1 (
    echo.
    echo [ERROR] Tests failed!
    exit /b 1
)
echo.
echo [INFO] Generating coverage report...
python -m coverage report --include=src/dynamic_signal_parser.py
goto done

:html
echo [INFO] Running regression tests and generating HTML report...
echo.
python -m coverage run -m unittest discover tests
if errorlevel 1 (
    echo.
    echo [ERROR] Tests failed!
    exit /b 1
)
echo.
echo [INFO] Generating HTML coverage report...
python -m coverage html --include=src/dynamic_signal_parser.py -d coverage_html
if not errorlevel 1 (
    echo.
    echo [SUCCESS] HTML coverage report generated in coverage_html\index.html
    echo [INFO] Open coverage_html\index.html in browser to view detailed report
)
goto done

:done
echo.
echo ============================================================
echo              Regression Tests Complete!
echo ============================================================
echo.
