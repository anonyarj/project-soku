import ollama
from config import MODEL_NAME
from memory import load_memories

SYSTEM_RULES = """
Your name is Soku.
You are a private, local-first personal AI assistant.

Rules:
- You have local persistent memory supplied by the Python application.
- Never invent or guess personal facts.
- Only use personal facts present in the supplied memory.
- If a fact is unknown, say you do not know it yet.
- Never claim an action was completed unless Python actually completed it.
- Never claim to send messages, place calls, delete files, buy things, or change
  system settings unless an authorized tool reports success.
- Be concise, natural, and conversational.
"""

def memory_context():
    saved = load_memories()
    if not saved:
        return "Saved user memory: none."
    lines = "\n".join(f"- {key}: {value}" for key, value in saved)
    return "Saved user memory:\n" + lines

def ask_soku(conversation_messages):
    full_messages = [
        {
            "role": "system",
            "content": SYSTEM_RULES + "\n\n" + memory_context(),
        }
    ] + conversation_messages

    response = ollama.chat(
        model=MODEL_NAME,
        messages=full_messages,
    )
    return response["message"]["content"]
