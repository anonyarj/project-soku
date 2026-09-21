from faster_whisper import WhisperModel
import tempfile
import os


print("Loading Whisper model...")

whisper = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


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