import speech_recognition as sr
from faster_whisper import WhisperModel
import tempfile
import os

print("Loading Soku's speech model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak now...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source)

with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
    temp_file.write(audio.get_wav_data())
    temp_path = temp_file.name

print("Soku is understanding...")

segments, info = model.transcribe(temp_path)

text = " ".join(segment.text for segment in segments)

print("You said:", text)

os.remove(temp_path)