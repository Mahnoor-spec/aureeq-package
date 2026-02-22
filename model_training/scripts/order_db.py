import sqlite3
import os
import uuid
import datetime
from typing import Optional, List

SQLITE_PATH = "../../data/aureeq.db"

def get_db_connection():
    # Ensure directory exists
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Enable Wal mode for better concurrency
    cursor.execute("PRAGMA journal_mode=WAL")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            session_id TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT,
            dish_name TEXT,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()
    print("Database Initialized.")

def get_last_order(user_id: str) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT dish_name FROM orders WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
        row = cursor.fetchone()
        return row['dish_name'] if row else None
    except Exception as e:
        print(f"DB Error (get_last_order): {e}")
        return None
    finally: conn.close()

def save_order(user_id: str, dish_names: List[str], session_id: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Ensure user exists
        cursor.execute("INSERT OR IGNORE INTO users (user_id, session_id, created_at) VALUES (?, ?, ?)", 
                       (user_id, session_id, timestamp))
        
        for name in dish_names:
            order_id = str(uuid.uuid4())[:8]
            cursor.execute("INSERT INTO orders (order_id, user_id, dish_name, timestamp) VALUES (?, ?, ?, ?)", 
                           (order_id, user_id, name, timestamp))
        conn.commit()
    except Exception as e:
        print(f"DB Error (save_order): {e}")
    finally: conn.close()

if __name__ == "__main__":
    init_db()
