def detect_intent(command):

    command = command.lower().strip()

    # -------------------------
    # GET NAME
    # -------------------------

    name_questions = [
        "what is my name",
        "whats my name",
        "what's my name",
        "do you remember my name",
        "do you remember the name",
        "tell me my name",
        "who am i"
    ]

    for phrase in name_questions:
        if phrase in command:
            return "get_name", None


    # -------------------------
    # FORGET NAME
    # -------------------------

    forget_name_phrases = [
        "forget my name",
        "delete my name",
        "remove my name"
    ]

    for phrase in forget_name_phrases:
        if phrase in command:
            return "forget_name", None


    # -------------------------
    # SET NAME
    # -------------------------

    prefixes = [
        "my name is ",
        "save my name as ",
        "remember my name as ",
        "change my name to ",
        "update my name to "
    ]

    for prefix in prefixes:

        if command.startswith(prefix):

            value = command[
                len(prefix):
            ].strip()

            return "set_name", value


    # -------------------------
    # SHOW MEMORY
    # -------------------------

    memory_questions = [
        "what do you remember",
        "do you remember anything",
        "show memories",
        "show memory"
    ]

    for phrase in memory_questions:
        if phrase in command:
            return "show_memory", None


    return "chat", None
