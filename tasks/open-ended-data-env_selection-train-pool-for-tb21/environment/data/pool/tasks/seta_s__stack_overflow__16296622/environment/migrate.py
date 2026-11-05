#!/usr/bin/env python3
"""Simple SQL migration runner for SQLite."""

import os
import sys
import sqlite3
import glob

DB_PATH = "/app/data/app.db"
MIGRATIONS_DIR = "/app/migrations"


def run_migrations():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Create migrations tracking table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()

    # Get already applied migrations
    cursor.execute("SELECT filename FROM _migrations")
    applied = {row[0] for row in cursor.fetchall()}

    # Find and sort migration files
    sql_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))

    if not sql_files:
        print("No migration files found.")
        return

    for sql_file in sql_files:
        filename = os.path.basename(sql_file)
        if filename in applied:
            print(f"Skipping already applied: {filename}")
            continue

        print(f"Applying migration: {filename}")
        with open(sql_file, "r") as f:
            sql_content = f.read()

        try:
            cursor.executescript(sql_content)
            conn.commit()
            cursor.execute(
                "INSERT INTO _migrations (filename) VALUES (?)", (filename,)
            )
            conn.commit()
            print(f"  Success: {filename}")
        except Exception as e:
            print(f"  ERROR in {filename}: {e}", file=sys.stderr)
            conn.close()
            sys.exit(1)

    conn.close()
    print("All migrations applied successfully.")


if __name__ == "__main__":
    run_migrations()
