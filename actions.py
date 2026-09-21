import os
import subprocess
import webbrowser


def open_chrome():
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            return True

    return False


def open_calculator():
    subprocess.Popen(["calc.exe"])
    return True


def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return True


def open_vscode():
    try:
        subprocess.Popen(["code"])
        return True
    except FileNotFoundError:
        return False


def open_website(url):
    webbrowser.open(url)
    return True