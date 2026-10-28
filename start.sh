#!/usr/bin/env bash
# Social Media Content Hub: first run installs everything, later runs just start the app.
set -e
cd "$(dirname "$0")"

PY=""
for c in python3.13 python3.12 python3.11 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  echo "Python 3.11 or newer is required. Install it from https://www.python.org/downloads/ and run this again."
  exit 1
fi

if [ ! -x .venv/bin/streamlit ]; then
  echo "First run: setting things up (this takes a minute)..."
  "$PY" -m venv .venv
  .venv/bin/python -m pip install --upgrade pip --quiet
  .venv/bin/python -m pip install -r requirements.txt --quiet
fi

# Ask for a Creator Dashboard password if one isn't saved yet
.venv/bin/python set_password.py

echo "Starting the app. It will open in your browser at http://localhost:8501"
echo "Close this window (or press Ctrl+C) to stop it."
exec .venv/bin/streamlit run app.py "$@"
