"""Database module"""

import sqlite3

CONN = sqlite3.connect('database.db')
C = CONN.cursor()

C.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        token TEXT
    )
""")

C.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        start_date TEXT,
        end_date TEXT
    )
""")

CONN.commit()
