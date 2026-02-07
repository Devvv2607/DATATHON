@echo off
REM Activate virtual environment script for Windows

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Virtual environment not found at venv\Scripts\activate.bat
    echo Please create a virtual environment first with: python -m venv venv
)
