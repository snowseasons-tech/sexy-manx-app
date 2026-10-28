# Social Media Content Hub

Your fan question inbox, SnapDex contacts and Lens Vault, all in one app that runs on your own computer.

## Install and start

### 1. Install Python (one time only)

Download Python 3.11 or newer from <https://www.python.org/downloads/>.
On Windows, tick **"Add python.exe to PATH"** on the first screen of the installer.

### 2. Unzip this folder

Unzip it anywhere you like, such as your Desktop or Documents.

### 3. Start the app

- **Windows:** double-click `start.bat`
- **Mac / Linux:** open Terminal in this folder and run `./start.sh`

The first start takes a minute or two while it downloads what it needs. After that it starts in a few seconds. The app opens in your browser at <http://localhost:8501>.

On the first start, the app asks you to choose a password for the Creator Dashboard, then to type it again to confirm. Nothing appears on screen while you type; that is normal. The password is saved in `.streamlit/secrets.toml` inside the app folder.

To stop the app, close the black terminal window.

## Using it

- **Fan connect:** fans send questions. Open the **Creator Dashboard** tab and enter the password you chose at first start to reply, make story cards and publish answers.
- **SnapDex:** your contacts and streaks.
- **Lens Vault:** AR lenses. Your browser will ask for permission to use the camera.

Lens Vault and SnapDex need an internet connection for their fonts, icons and face tracking.

## Your data

- Fan questions are saved in `questions_db.json` in this folder. Copy that file to back them up.
- The name and stats in the sidebar come from `snapDex.json`. You can edit them in any text editor.

## Who can see it

This app only runs on this computer. Fans on other devices can't open it or send questions unless it is put online, which needs extra setup, so ask your developer.

## Troubleshooting

- **"Python 3.11 or newer is required":** install Python (step 1), then run the start file again.
- **Port already in use:** the app is probably already running in another window. Close that window first.
- **Something broke after an update:** delete the `.venv` folder and run the start file again to reinstall.
- **Forgot the password, or want to change it:** delete `.streamlit/secrets.toml` and run the start file again. It will ask for a new one. The `.streamlit` folder is hidden on Mac and Linux; press Cmd+Shift+. in Finder to show it.
- **Dashboard says it's locked:** close the app and run the start file again. It will ask you to choose a password.
