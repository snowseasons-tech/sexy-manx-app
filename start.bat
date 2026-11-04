@echo off
rem Social Media Content Hub: first run installs everything, later runs just start the app.
cd /d "%~dp0"

if exist ".venv\Scripts\streamlit.exe" goto run

set "PY="
where py >nul 2>&1 && py -3 -c "import sys; sys.exit(sys.version_info < (3, 11))" >nul 2>&1 && set "PY=py -3"
if not defined PY (
  where python >nul 2>&1 && python -c "import sys; sys.exit(sys.version_info < (3, 11))" >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo Python 3.11 or newer is required.
  echo Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH", then run this again.
  pause
  exit /b 1
)

echo First run: setting things up (this takes a minute)...
%PY% -m venv .venv || goto fail
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet || goto fail

:run
rem Ask for a Creator Dashboard password if one isn't saved yet
".venv\Scripts\python.exe" set_password.py || goto fail
echo Starting the app. It will open in your browser at http://localhost:8501
echo Close this window to stop it.
".venv\Scripts\streamlit.exe" run app.py %*
pause
exit /b 0

:fail
echo Setup failed. Check your internet connection and try again.
pause
exit /b 1
