import sqlite3
from config import MEMORY_DB

def _connect():
    return sqlite3.connect(MEMORY_DB)

def setup_memory():
    with _connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profile_memory (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.commit()

def save_memory(key, value):
    with _connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO profile_memory (key, value)
            VALUES (?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        connection.commit()

def get_memory(key):
    with _connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT value FROM profile_memory WHERE key = ?",
            (key,),
        )
        result = cursor.fetchone()
    return result[0] if result else None

def delete_memory(key):
    with _connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM profile_memory WHERE key = ?",
            (key,),
        )
        connection.commit()

def load_memories():
    with _connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT key, value FROM profile_memory ORDER BY key")
        return cursor.fetchall()

def show_memories():
    memories = load_memories()
    if not memories:
        return "I don't have any saved personal information yet."
    return "\n".join(f"{key}: {value}" for key, value in memories)
