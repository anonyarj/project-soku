import speech_recognition as sr

from actions import media, open_app, open_website, scroll
from brain import ask_soku
from config import EXIT_COMMANDS, SLEEP_COMMANDS
from intent import detect_intent
from memory import (
    delete_memory,
    get_memory,
    save_memory,
    setup_memory,
    show_memories,
)
from voice_input import transcribe_audio
from voice_output import speak, speak_async
from wake_word import clean_text, is_wake_word

setup_memory()

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.8

messages = []

def reply(text, async_voice=False):
    print("Soku:", text)
    if async_voice:
        speak_async(text)
    else:
        speak(text)

def listen_for_phrase(source, timeout, phrase_time_limit):
    try:
        return recognizer.listen(
            source,
            timeout=timeout,
            phrase_time_limit=phrase_time_limit,
        )
    except sr.WaitTimeoutError:
        return None

print("\nSoku is sleeping.")
print("Say 'Hey Soku' to wake me.")

while True:
    # -------------------------
    # SLEEP MODE
    # -------------------------
    while True:
        with sr.Microphone() as source:
            print("\nListening for wake word...")
            recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = listen_for_phrase(source, timeout=10, phrase_time_limit=5)

        if audio is None:
            continue

        wake_text = transcribe_audio(audio, force_english=True)
        print("Heard:", wake_text)

        if wake_text and is_wake_word(wake_text):
            reply("Yes?")
            break

    print("\nSoku is awake.")

    # -------------------------
    # AWAKE MODE
    # -------------------------
    while True:
        with sr.Microphone() as source:
            print("\nListening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.25)
            command_audio = listen_for_phrase(
                source,
                timeout=20,
                phrase_time_limit=25,
            )

        if command_audio is None:
            print("No speech detected.")
            continue

        print("Understanding...")
        user_message = transcribe_audio(command_audio)

        if not user_message:
            reply("I didn't catch that.")
            continue

        print("You:", user_message)
        command = clean_text(user_message)

        if any(x in command for x in SLEEP_COMMANDS):
            reply("Going to sleep.")
            print("\nSoku is sleeping again.")
            break

        if any(x in command for x in EXIT_COMMANDS):
            reply("Goodbye.")
            raise SystemExit

        intent, value = detect_intent(command)

        # Memory
        if intent == "set_name":
            save_memory("name", value)
            reply(f"I'll remember that your name is {value}.")
            continue

        if intent == "get_name":
            name = get_memory("name")
            reply(
                f"Your name is {name}."
                if name
                else "I don't have your name saved yet."
            )
            continue

        if intent == "forget_name":
            delete_memory("name")
            reply("I forgot your saved name.")
            continue

        if intent == "show_memory":
            reply(show_memories())
            continue

        # Secure actions
        if intent == "open_app":
            _, message = open_app(value)
            reply(message)
            continue

        if intent == "open_website":
            _, message = open_website(value)
            reply(message)
            continue

        if intent == "scroll":
            _, message = scroll(value)
            reply(message)
            continue

        if intent == "media":
            _, message = media(value)
            reply(message)
            continue

        # General local-AI conversation
        messages.append({"role": "user", "content": user_message})

        try:
            soku_reply = ask_soku(messages)
        except Exception as error:
            print("Soku AI error:", error)
            reply("I had a problem running my local AI model.")
            continue

        messages.append({"role": "assistant", "content": soku_reply})

        # Asynchronous voice is a first step toward interruption/barge-in.
        reply(soku_reply, async_voice=True)
