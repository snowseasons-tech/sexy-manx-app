#!/usr/bin/env bash
# Builds dist/social-media-content-hub.zip to hand to the client.
set -e
cd "$(dirname "$0")"
NAME=social-media-content-hub
rm -rf dist && mkdir -p "dist/$NAME"
cp -r app.py app_pages set_password.py requirements.txt snapDex.json lens_vault.html \
  snapchat_contact_streak_manager.html .streamlit start.sh start.bat README.md LICENSE "dist/$NAME/"
rm -f "dist/$NAME/.streamlit/secrets.toml"
find "dist/$NAME" -name __pycache__ -prune -exec rm -rf {} +
(cd dist && zip -qr "$NAME.zip" "$NAME")
rm -rf "dist/$NAME"
unzip -l "dist/$NAME.zip" | grep -q "secrets.toml$" && { echo "secrets.toml leaked into the zip"; exit 1; }
echo "Built dist/$NAME.zip"
