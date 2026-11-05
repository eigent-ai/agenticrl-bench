"""SQLite database backend for game state persistence."""

import sqlite3
import json


class GameDatabase:
    """SQLite-backed storage for game entities."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS entities")
        cursor.execute("""
            CREATE TABLE entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save_entity(self, entity_data):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO entities (name, class_name, entity_type, data) VALUES (?, ?, ?, ?)",
            (
                entity_data["name"],
                entity_data["class"],
                entity_data["entity_type"],
                json.dumps(entity_data),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def load_all_entities(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM entities")
        rows = cursor.fetchall()
        return [json.loads(row["data"]) for row in rows]

    def load_entity_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM entities WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return json.loads(row["data"])
        return None

    def close(self):
        self.conn.close()
