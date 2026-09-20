import ollama
import pyttsx3
import speech_recognition as sr
from faster_whisper import WhisperModel
from difflib import SequenceMatcher
import tempfile
import os
from voice_output import speak

from memory import (
    setup_memory,
    save_memory,
    load_memories,
    show_memories
)



# =========================================================
# SETTINGS
# =========================================================

WAKE_WORD_TARGETS = [
    "hey soku",
    "hi soku",
    "soku"
]

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
setup_memory()

# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    text = text.lower().strip()

    for symbol in [
        ",",
        ".",
        "!",
        "?",
        "'",
        '"'
    ]:
        text = text.replace(symbol, "")

    return text


# =========================================================
# WAKE WORD MATCHING
# =========================================================

def is_wake_word(text):
    text = clean_text(text)

    for target in WAKE_WORD_TARGETS:

        similarity = SequenceMatcher(
            None,
            text,
            target
        ).ratio()

        print(
            f"Wake similarity with '{target}': "
            f"{similarity:.2f}"
        )

        if similarity >= 0.60:
            return True

    return False


# =========================================================
# MICROPHONE
# =========================================================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.8


# =========================================================
# WHISPER
# =========================================================

print("Loading Soku speech model...")

whisper = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


# =========================================================
# SPEECH TO TEXT
# =========================================================

def transcribe_audio(audio, force_english=False):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_file:

        temp_file.write(
            audio.get_wav_data()
        )

        temp_path = temp_file.name

    try:

        if force_english:

            segments, info = whisper.transcribe(
                temp_path,
                language="en"
            )

        else:

            segments, info = whisper.transcribe(
                temp_path
            )

        text = " ".join(
            segment.text
            for segment in segments
        ).strip()

        return text

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


# =========================================================
# LOAD SAVED MEMORIES
# =========================================================

saved_memories = load_memories()

memory_context = ""

if saved_memories:
    memory_context = "\nKnown information about the user:\n"

    for memory in saved_memories:
        memory_context += f"- {memory}\n"


# =========================================================
# CONVERSATION MEMORY
# =========================================================

messages = [
    {
        "role": "system",
        "content": (
            "Your name is Soku. "
            "You are a private personal AI assistant. "
            "You run locally on the user's computer. "
            "You wake when the user says Hey Soku or a similar phrase. "
            "Once awake, you stay awake for conversation. "
            "You return to sleep only when the user asks you to sleep. "
            "Be helpful, concise, and conversational."
            + memory_context
        )
    }
]


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


        # =================================================
        # SLEEP COMMAND
        # =================================================

        if any(
            sleep_command in command
            for sleep_command in SLEEP_COMMANDS
        ):

            print("Soku: Going to sleep.")
            speak("Going to sleep.")

            print(
                "\nSoku is sleeping again."
            )

            break


        # =================================================
        # EXIT PROGRAM
        # =================================================

        if any(
            exit_command in command
            for exit_command in EXIT_COMMANDS
        ):

            print("Soku: Goodbye.")
            speak("Goodbye.")

            raise SystemExit


        # =================================================
        # SAVE MEMORY
        # =================================================

        if command.startswith("remember that "):

            memory = user_message[
                len("remember that "):
            ].strip()

            if memory:

                save_memory(memory)

                print(
                    f"Soku: I will remember that {memory}."
                )

                speak(
                    f"I will remember that {memory}."
                )

            continue


        # =================================================
        # SHOW MEMORY
        # =================================================

        if (
            "what do you remember" in command
            or "show memories" in command
            or "show memory" in command
        ):

            memories = show_memories()

            print(
                "Soku memory:"
            )

            print(
                memories
            )

            speak(
                memories
            )

            continue


        # =================================================
        # USER MESSAGE
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

        response = ollama.chat(
            model="phi3",
            messages=messages
        )


        soku_reply = response[
            "message"
        ][
            "content"
        ]


        # =================================================
        # SAVE RESPONSE
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