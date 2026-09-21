import sqlite3


DB_NAME = "soku_memory.db"


def setup_memory():
    connection = sqlite3.connect(DB_NAME)
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
    connection.close()


def save_memory(key, value):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO profile_memory (key, value)
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
        """,
        (key, value)
    )

    connection.commit()
    connection.close()


def get_memory(key):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT value
        FROM profile_memory
        WHERE key = ?
        """,
        (key,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def delete_memory(key):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM profile_memory
        WHERE key = ?
        """,
        (key,)
    )

    connection.commit()
    connection.close()


def load_memories():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT key, value
        FROM profile_memory
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def show_memories():
    memories = load_memories()

    if not memories:
        return "I don't have any saved personal information yet."

    return "\n".join(
        f"{key}: {value}"
        for key, value in memories
    )