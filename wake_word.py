from difflib import SequenceMatcher


WAKE_WORD_TARGETS = [
    "hey soku",
    "hi soku",
    "soku"
    "hey cool"
    "so cool"
]


def clean_text(text):
    text = text.lower().strip()

    for symbol in [",", ".", "!", "?", "'", '"']:
        text = text.replace(symbol, "")

    return text


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