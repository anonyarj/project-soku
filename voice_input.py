import os
import tempfile
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE

print("Loading Whisper model...")

whisper = WhisperModel(
    WHISPER_MODEL,
    device=WHISPER_DEVICE,
    compute_type=WHISPER_COMPUTE_TYPE,
)

def transcribe_audio(audio, force_english=False):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio.get_wav_data())
        temp_path = temp_file.name

    try:
        kwargs = {"language": "en"} if force_english else {}
        segments, _ = whisper.transcribe(temp_path, **kwargs)
        return " ".join(segment.text for segment in segments).strip()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
