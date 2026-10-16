from difflib import SequenceMatcher
from config import WAKE_WORD_TARGETS, WAKE_THRESHOLD

def clean_text(text):
    text = (text or "").lower().strip()
    for symbol in [",", ".", "!", "?", "'", '"', ":", ";"]:
        text = text.replace(symbol, "")
    return " ".join(text.split())

def is_wake_word(text):
    text = clean_text(text)
    if not text:
        return False

    for target in WAKE_WORD_TARGETS:
        target_clean = clean_text(target)

        if target_clean in text:
            return True

        similarity = SequenceMatcher(None, text, target_clean).ratio()
        print(f"Wake similarity with '{target}': {similarity:.2f}")

        if similarity >= WAKE_THRESHOLD:
            return True

    return False
