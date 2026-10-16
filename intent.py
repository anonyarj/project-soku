def detect_intent(command):
    command = (command or "").lower().strip()

    # =====================================================
    # NAME MEMORY - GET
    # =====================================================

    name_questions = [
        "what is my name",
        "whats my name",
        "what's my name",
        "do you remember my name",
        "do you remember the name",
        "tell me my name",
        "who am i",
    ]

    for phrase in name_questions:
        if phrase in command:
            return "get_name", None

    # =====================================================
    # NAME MEMORY - FORGET
    # =====================================================

    forget_name_phrases = [
        "forget my name",
        "delete my name",
        "remove my name",
    ]

    for phrase in forget_name_phrases:
        if phrase in command:
            return "forget_name", None

    # =====================================================
    # NAME MEMORY - SAVE / UPDATE
    # =====================================================

    name_prefixes = [
        "my name is ",
        "save my name as ",
        "remember my name as ",
        "change my name to ",
        "update my name to ",
    ]

    for prefix in name_prefixes:
        if command.startswith(prefix):
            value = command[len(prefix):].strip(" .,!?:;")
            return "set_name", value

    # =====================================================
    # SHOW MEMORY
    # =====================================================

    memory_questions = [
        "what do you remember",
        "do you remember anything",
        "show memories",
        "show memory",
        "what have you saved",
        "what do you know about me",
    ]

    for phrase in memory_questions:
        if phrase in command:
            return "show_memory", None

    # =====================================================
    # OPEN APPLICATIONS
    # =====================================================

    if "open" in command:

        if "chrome" in command:
            return "open_app", "chrome"

        if "calculator" in command:
            return "open_app", "calculator"

        if "notepad" in command:
            return "open_app", "notepad"

        if (
            "vs code" in command
            or "vscode" in command
            or "visual studio code" in command
        ):
            return "open_app", "vscode"

    # =====================================================
    # OPEN WEBSITES
    # =====================================================

    if "open" in command:

        if "facebook" in command:
            return "open_website", "https://www.facebook.com"

        if "youtube" in command:
            return "open_website", "https://www.youtube.com"

        if "github" in command:
            return "open_website", "https://github.com"

        if "google" in command and "chrome" not in command:
            return "open_website", "https://www.google.com"

    # =====================================================
    # SCROLL
    # =====================================================

    if "scroll down" in command:
        return "scroll", "down"

    if "scroll up" in command:
        return "scroll", "up"

    # =====================================================
    # MEDIA CONTROL
    # =====================================================

    if (
        "pause video" in command
        or "play video" in command
        or "play pause" in command
        or "pause this" in command
    ):
        return "media", "play_pause"

    if (
        "next video" in command
        or "next reel" in command
        or "next one" in command
    ):
        return "media", "next"

    if (
        "previous video" in command
        or "previous reel" in command
        or "go back one" in command
    ):
        return "media", "previous"

    if "volume up" in command:
        return "media", "volume_up"

    if "volume down" in command:
        return "media", "volume_down"

    if "mute" in command:
        return "media", "mute"

    # =====================================================
    # DEFAULT: NORMAL CHAT
    # =====================================================

    return "chat", None