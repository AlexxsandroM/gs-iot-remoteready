import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "chatbot.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_message TEXT NOT NULL,
                bot_answer  TEXT NOT NULL,
                created_at  TEXT NOT NULL
            );
        """)
        conn.commit()

def save_message(user_id: int, user_message: str, bot_answer: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_history (user_id, user_message, bot_answer, created_at)
            VALUES (?, ?, ?, ?);
        """, (user_id, user_message, bot_answer, datetime.utcnow().isoformat()))
        conn.commit()
