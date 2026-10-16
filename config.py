MODEL_NAME = "phi3"

WHISPER_MODEL = "base"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

WAKE_THRESHOLD = 0.60
WAKE_WORD_TARGETS = [
    "hey soku",
    "hi soku",
    "soku",
    "hey so cool",
    "hi so cool",
    "so cool",
]

SLEEP_COMMANDS = [
    "go to sleep",
    "sleep",
    "stop listening",
    "go back to sleep",
    "sleep now",
]

EXIT_COMMANDS = [
    "exit",
    "quit",
    "goodbye",
    "shut down",
    "shutdown",
]

# Security: keep this False unless you intentionally want browser URLs opened.
ALLOW_WEBSITE_OPEN = True

# Experimental features. Turn on only after installing optional dependencies.
ENABLE_VISION = False
ENABLE_GESTURES = False

MEMORY_DB = "soku_memory.db"
ACTION_LOG = "soku_actions.log"
