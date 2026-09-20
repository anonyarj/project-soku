import sqlite3

DB_NAME = "soku_memory.db"


def setup_memory():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_memory(memory):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO memories (memory) VALUES (?)",
        (memory,)
    )

    connection.commit()
    connection.close()


def load_memories():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT memory FROM memories")
    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]


def show_memories():
    memories = load_memories()

    if not memories:
        return "I don't have any saved memories yet."

    return "\n".join(
        f"- {memory}"
        for memory in memories
    )