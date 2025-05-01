@echo off
setlocal

echo Starting Agriculture Blockchain Project...

REM Basic Python Version Check (Advisory)
FOR /F "tokens=1,2 delims=." %%A IN ('python --version 2^>^&1') DO (
    set PYTHON_MAJOR=%%A
    set PYTHON_MINOR=%%B
)

REM Extract major version number (handle potential text like 'Python 3')
for /f "tokens=2" %%i in ("%PYTHON_MAJOR%") do set PYTHON_MAJOR_NUM=%%i

REM Check if major/minor numbers were found
if not defined PYTHON_MAJOR_NUM (
    echo WARNING: Could not reliably determine Python major version.
) else if not defined PYTHON_MINOR (
    echo WARNING: Could not reliably determine Python minor version.
) else (
    echo Found Python Version: %PYTHON_MAJOR_NUM%.%PYTHON_MINOR%
    if %PYTHON_MAJOR_NUM% GEQ 3 (
        if %PYTHON_MINOR% GEQ 12 (
            echo **********************************************************************
            echo WARNING: Python 3.12+ detected (%PYTHON_MAJOR_NUM%.%PYTHON_MINOR%).
            echo This project uses Django 2.1.7 which is INCOMPATIBLE with Python 3.12+
            echo due to removed modules (distutils, cgi).
            echo Please use a Python environment like 3.8, 3.9, 3.10, or 3.11.
            echo Pausing execution. Press Ctrl+C to abort or any key to attempt...
            echo **********************************************************************
            pause > nul
        )
    )
)

REM Check for .env file
if not exist ".env" (
    echo ERROR: .env file not found.
    echo Please copy .env.example to .env and fill in the required values:
    echo   - SECRET_KEY (Generate a strong random key for Django)
    echo   - ENCRYPTION_KEY (Generate a 32-byte hex-encoded key for AES)
    echo.
    echo Example command to generate AES key:
    echo   python -c "import secrets; print(secrets.token_hex(32))"
    echo.
    pause
    exit /b 1
)

echo Installing required dependencies from requirements.txt...
python -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo Creating necessary directories...
if not exist "media" mkdir media
if not exist "static" mkdir static

echo Collecting static files...
python manage.py collectstatic --noinput

if %ERRORLEVEL% NEQ 0 (
    echo WARNING: collectstatic command failed. Static files might be missing.
    REM Do not exit here, maybe the server can still run for development
)

echo Running migrations...
python manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to run migrations.
    pause
    exit /b 1
)

echo Starting the server...
python manage.py runserver

echo Server stopped.
pause
endlocal 