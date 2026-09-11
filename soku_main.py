import ollama
import pyttsx3
import speech_recognition as sr
from faster_whisper import WhisperModel
import tempfile
import os


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


recognizer = sr.Recognizer()

whisper = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

messages = [
    {
        "role": "system",
        "content": (
            "Your name is Soku. "
            "You are a private personal AI assistant. "
            "Be helpful, concise, and conversational."
        )
    }
]

print("Soku is ready.")
speak("Soku is ready.")

while True:

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio.get_wav_data())
        temp_path = temp_file.name

    print("Understanding...")

    segments, info = whisper.transcribe(temp_path)

    user_message = " ".join(
        segment.text for segment in segments
    ).strip()

    os.remove(temp_path)

    if not user_message:
        print("Soku: I didn't catch that.")
        speak("I didn't catch that.")
        continue

    print("You:", user_message)

    if user_message.lower() in [
        "exit",
        "quit",
        "bye",
        "goodbye"
    ]:
        print("Soku: Goodbye.")
        speak("Goodbye.")
        break

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = ollama.chat(
        model="phi3",
        messages=messages
    )

    soku_reply = response["message"]["content"]

    messages.append(
        {
            "role": "assistant",
            "content": soku_reply
        }
    )

    print("Soku:", soku_reply)

    speak(soku_reply)