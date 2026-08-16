@echo off
setlocal
cd /d %~dp0
if not exist venv\Scripts\activate.bat (
  echo Create the virtual environment first: py -3.11 -m venv venv
  pause
  exit /b 1
)
call venv\Scripts\activate.bat
python backend\run.py
