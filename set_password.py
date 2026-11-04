"""Make sure .streamlit/secrets.toml holds a Creator Dashboard password, asking for one if it doesn't.

Run by start.sh / start.bat before the app starts. Pass --reset to choose a new password.
"""
import getpass
import json
import os
import sys
import tomllib
from pathlib import Path

SECRETS_FILE = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"


def current_password():
    try:
        with open(SECRETS_FILE, "rb") as f:
            password = tomllib.load(f).get("creator_password")
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    return password if isinstance(password, str) and password else None


def ask_password():
    while True:
        password = getpass.getpass("Choose a password for the Creator Dashboard: ")
        if not password:
            print("The password can't be empty. Try again.")
        elif getpass.getpass("Type it again to confirm: ") != password:
            print("Those didn't match. Try again.")
        else:
            return password


def save_password(password):
    SECRETS_FILE.parent.mkdir(exist_ok=True)
    tmp = SECRETS_FILE.with_suffix(".tmp")
    # A JSON string is also a valid TOML basic string, so json.dumps handles all escaping
    tmp.write_text(f"creator_password = {json.dumps(password)}\n", encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, SECRETS_FILE)


if __name__ == "__main__":
    if "--reset" in sys.argv or current_password() is None:
        save_password(ask_password())
        print("Password saved.")
