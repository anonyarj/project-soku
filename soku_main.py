import speech_recognition as sr

from voice_output import speak
from wake_word import is_wake_word, clean_text
from memory import (
    setup_memory,
    save_memory,
    get_memory,
    delete_memory,
    load_memories,
    show_memories
)
from brain import ask_soku
from voice_input import transcribe_audio

from intent import detect_intent


# =========================================================
# SETTINGS
# =========================================================

SLEEP_COMMANDS = [
    "go to sleep",
    "sleep",
    "stop listening",
    "go back to sleep",
    "sleep now"
]

EXIT_COMMANDS = [
    "exit",
    "quit",
    "goodbye",
    "shut down",
    "shutdown"
]


# =========================================================
# INITIALIZE MEMORY
# =========================================================

setup_memory()


# =========================================================
# MICROPHONE SETTINGS
# =========================================================

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.8


# =========================================================
# LOAD SAVED MEMORY INTO AI CONTEXT
# =========================================================

saved_memories = load_memories()

memory_context = ""

if saved_memories:
    memory_context = "\nSaved information about the user:\n"

    for key, value in saved_memories:
        memory_context += f"- {key}: {value}\n"


# =========================================================
# CONVERSATION SESSION
# =========================================================

messages = [
    {
        "role": "system",
        "content": (
            "Your name is Soku. "
            "You are a private, local-first personal AI assistant. "
            "Be helpful, concise, natural, and conversational. "
            "Never invent or guess personal information about the user. "
            "Only claim to know personal information if it exists in saved memory. "
            "If you do not know a personal fact, say that you do not know it yet. "
            "Never claim that you saved, deleted, opened, changed, or performed "
            "an action unless the Python system actually performed that action. "
            "Once awake, remain awake until the user explicitly asks you to sleep."
            + memory_context
        )
    }
]


# =========================================================
# REFRESH MEMORY CONTEXT
# =========================================================

def refresh_memory_context():
    saved = load_memories()

    context = "\nSaved information about the user:\n"

    if not saved:
        context += "- No saved personal information.\n"

    else:
        for key, value in saved:
            context += f"- {key}: {value}\n"

    messages[0]["content"] = (
        "Your name is Soku. "
        "You are a private, local-first personal AI assistant. "
        "Be helpful, concise, natural, and conversational. "
        "Never invent or guess personal information about the user. "
        "Only claim to know personal information if it exists in saved memory. "
        "If you do not know a personal fact, say that you do not know it yet. "
        "Never claim that you saved, deleted, opened, changed, or performed "
        "an action unless the Python system actually performed that action. "
        "Once awake, remain awake until the user explicitly asks you to sleep."
        + context
    )


# =========================================================
# START
# =========================================================

print("\nSoku is sleeping.")
print("Say 'Hey Soku' to wake me.")


while True:

    # =====================================================
    # SLEEP MODE
    # =====================================================

    while True:

        with sr.Microphone() as source:

            print("\nListening for wake word...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            try:
                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=5
                )

            except sr.WaitTimeoutError:
                continue


        wake_text = transcribe_audio(
            audio,
            force_english=True
        )

        print("Heard:", wake_text)

        if not wake_text:
            continue


        if is_wake_word(wake_text):

            print("Soku: Yes?")
            speak("Yes?")

            break


    # =====================================================
    # AWAKE MODE
    # =====================================================

    print("\nSoku is awake.")


    while True:

        with sr.Microphone() as source:

            print("\nListening for command...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.3
            )

            try:
                command_audio = recognizer.listen(
                    source,
                    timeout=15,
                    phrase_time_limit=20
                )

            except sr.WaitTimeoutError:
                print("No speech detected.")
                continue


        print("Understanding...")


        user_message = transcribe_audio(
            command_audio
        )


        if not user_message:

            print("Soku: I didn't catch that.")
            speak("I didn't catch that.")

            continue


        print("You:", user_message)


        command = clean_text(
            user_message
        )

        intent, value = detect_intent(command)

        # =================================================
        # SLEEP COMMAND
        # =================================================

        if any(
            sleep_command in command
            for sleep_command in SLEEP_COMMANDS
        ):

            print("Soku: Going to sleep.")
            speak("Going to sleep.")

            print("\nSoku is sleeping again.")

            break


        # =================================================
        # EXIT COMMAND
        # =================================================

        if any(
            exit_command in command
            for exit_command in EXIT_COMMANDS
        ):

            print("Soku: Goodbye.")
            speak("Goodbye.")

            raise SystemExit


        # =================================================
        # SAVE / UPDATE USER NAME
        # =================================================

        name = None

        if command.startswith("my name is "):

            name = user_message[
                len("my name is "):
            ].strip()


        elif command.startswith("save my name as "):

            name = user_message[
                len("save my name as "):
            ].strip()


        elif command.startswith("remember my name as "):

            name = user_message[
                len("remember my name as "):
            ].strip()


        elif command.startswith("change my name to "):

            name = user_message[
                len("change my name to "):
            ].strip()


        elif command.startswith("update my name to "):

            name = user_message[
                len("update my name to "):
            ].strip()


        if name:

            name = name.rstrip(".,!?")

            save_memory(
                "name",
                name
            )

            refresh_memory_context()

            reply = (
                f"I'll remember that your name is {name}."
            )

            print("Soku:", reply)
            speak(reply)

            continue


        # =================================================
        # ASK USER NAME
        # =================================================

        if (
            "what is my name" in command
            or "whats my name" in command
            or "do you remember the name" in command
            or "do you remember my name" in command
        ):

            name = get_memory(
                "name"
            )

            if name:
                reply = f"Your name is {name}."

            else:
                reply = (
                    "I don't have your name saved yet."
                )

            print("Soku:", reply)
            speak(reply)

            continue


        # =================================================
        # FORGET USER NAME
        # =================================================

        if (
            "forget my name" in command
            or "delete my name" in command
            or "remove my name" in command
        ):

            delete_memory(
                "name"
            )

            refresh_memory_context()

            reply = (
                "I forgot your saved name."
            )

            print("Soku:", reply)
            speak(reply)

            continue


        # =================================================
        # SHOW SAVED MEMORY
        # =================================================

        if (
            "what do you remember" in command
            or "do you remember anything" in command
            or "show memories" in command
            or "show memory" in command
        ):

            memories = show_memories()

            print("\nSoku memory:")
            print(memories)

            speak(memories)

            continue


        # =================================================
        # ADD USER MESSAGE TO SESSION MEMORY
        # =================================================

        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )


        # =================================================
        # ASK LOCAL AI
        # =================================================

        try:

            soku_reply = ask_soku(
                messages
            )

        except Exception as error:

            print(
                "\nSoku AI error:",
                error
            )

            speak(
                "I had a problem running my local AI model."
            )

            continue


        # =================================================
        # SAVE RESPONSE IN SESSION MEMORY
        # =================================================

        messages.append(
            {
                "role": "assistant",
                "content": soku_reply
            }
        )


        # =================================================
        # OUTPUT
        # =================================================

        print(
            "Soku:",
            soku_reply
        )

        speak(
            soku_reply
        )