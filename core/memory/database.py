"""
=========================================
JARVIS MEMORY DATABASE
=========================================
"""

import sqlite3
from pathlib import Path


class MemoryDatabase:

    def __init__(self):

        self.db_path = Path("data") / "memory.db"

        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                content TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()

    def close(self):

        self.connection.close()
    def save_memory(self, content):

        self.cursor.execute(
            """
            INSERT INTO memories (content)
            VALUES (?)
            """,
            (content,),
        )

        self.connection.commit()
    def update_memory(self, old_content, new_content):

        self.cursor.execute(
            """
            UPDATE memories
            SET content = ?
            WHERE content = ?
            """,
            (new_content, old_content),
        )

        self.connection.commit()

        return self.cursor.rowcount > 0
    def get_all_memories(self):

        self.cursor.execute("""
            SELECT content
            FROM memories
            ORDER BY created_at
        """)

        rows = self.cursor.fetchall()

        return [row[0] for row in rows]