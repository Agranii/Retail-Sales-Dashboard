@echo off
title Retail Sales Dashboard Launcher
echo ===================================================
echo        Starting Retail Sales Dashboard...
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please make sure Python 3.9+ is installed and added to PATH.
    pause
    exit /b
)

:: Run streamlit app
echo Launching Streamlit dashboard in default browser...
streamlit run app.py

pause

