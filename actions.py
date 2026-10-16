import os
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

from config import ACTION_LOG, ALLOW_WEBSITE_OPEN
from security import app_allowed, url_allowed

def _log(action, detail, success):
    line = f"{datetime.now().isoformat(timespec='seconds')} | {action} | {detail} | {success}\n"
    with open(ACTION_LOG, "a", encoding="utf-8") as f:
        f.write(line)

def open_app(app_name):
    app = app_name.lower().strip()

    if not app_allowed(app):
        _log("open_app", app, False)
        return False, f"{app_name} is not in my allowed-app list."

    try:
        if app == "calculator":
            subprocess.Popen(["calc.exe"])
        elif app == "notepad":
            subprocess.Popen(["notepad.exe"])
        elif app == "vscode":
            subprocess.Popen(["code"])
        elif app == "chrome":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            chrome = next((p for p in paths if os.path.exists(p)), None)
            if chrome:
                subprocess.Popen([chrome])
            else:
                subprocess.Popen(["cmd", "/c", "start", "", "chrome"])
        else:
            return False, "That application is not configured."

        _log("open_app", app, True)
        return True, f"Opening {app_name}."
    except Exception as exc:
        _log("open_app", f"{app}: {exc}", False)
        return False, f"I couldn't open {app_name}."

def open_website(url):
    if not ALLOW_WEBSITE_OPEN:
        return False, "Opening websites is disabled in configuration."

    if not url_allowed(url):
        _log("open_website", url, False)
        return False, "That website is not on my allowed-domain list."

    try:
        webbrowser.open(url)
        _log("open_website", url, True)
        return True, "Opening the website."
    except Exception as exc:
        _log("open_website", f"{url}: {exc}", False)
        return False, "I couldn't open that website."

def scroll(direction, amount=5):
    try:
        import pyautogui
    except ImportError:
        return False, "PyAutoGUI is not installed."

    clicks = abs(int(amount))
    if direction == "down":
        clicks = -clicks
    elif direction != "up":
        return False, "Unknown scroll direction."

    pyautogui.scroll(clicks)
    _log("scroll", f"{direction}:{amount}", True)
    return True, f"Scrolling {direction}."

def media(action):
    try:
        import pyautogui
    except ImportError:
        return False, "PyAutoGUI is not installed."

    mapping = {
        "play_pause": "playpause",
        "next": "nexttrack",
        "previous": "prevtrack",
        "volume_up": "volumeup",
        "volume_down": "volumedown",
        "mute": "volumemute",
    }
    key = mapping.get(action)
    if not key:
        return False, "Unknown media action."

    pyautogui.press(key)
    _log("media", action, True)
    return True, "Done."
