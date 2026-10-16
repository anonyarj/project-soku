from urllib.parse import urlparse

ALLOWED_APPS = {
    "chrome",
    "calculator",
    "notepad",
    "vscode",
}

ALLOWED_WEB_SCHEMES = {"https"}

# Add domains you intentionally want Soku to open.
ALLOWED_DOMAINS = {
    "facebook.com",
    "www.facebook.com",
    "youtube.com",
    "www.youtube.com",
    "google.com",
    "www.google.com",
    "github.com",
    "www.github.com",
}

HIGH_RISK_ACTIONS = {
    "delete_file",
    "send_message",
    "purchase",
    "install_software",
    "run_shell",
    "change_security_setting",
}

def app_allowed(app_name: str) -> bool:
    return app_name.lower() in ALLOWED_APPS

def url_allowed(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme.lower() not in ALLOWED_WEB_SCHEMES:
            return False
        host = (parsed.hostname or "").lower()
        return host in ALLOWED_DOMAINS
    except Exception:
        return False

def requires_confirmation(action_name: str) -> bool:
    return action_name in HIGH_RISK_ACTIONS
