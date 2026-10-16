import threading
import pyttsx3

class Speaker:
    """
    Threaded TTS wrapper.

    say_async() allows Soku to speak without blocking the main program.
    stop() requests interruption. pyttsx3 interruption behavior can vary by
    Windows voice driver, so treat barge-in as best-effort in this version.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._thread = None
        self._engine = None

    def _speak_worker(self, text):
        with self._lock:
            try:
                self._engine = pyttsx3.init()
                self._engine.say(str(text))
                self._engine.runAndWait()
            finally:
                try:
                    if self._engine:
                        self._engine.stop()
                except Exception:
                    pass
                self._engine = None

    def say(self, text):
        self.stop()
        self._speak_worker(text)

    def say_async(self, text):
        self.stop()
        self._thread = threading.Thread(
            target=self._speak_worker,
            args=(text,),
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        try:
            if self._engine is not None:
                self._engine.stop()
        except Exception:
            pass

    def is_speaking(self):
        return bool(self._thread and self._thread.is_alive())

speaker = Speaker()

def speak(text):
    speaker.say(text)

def speak_async(text):
    speaker.say_async(text)

def stop_speaking():
    speaker.stop()
