import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional

DB_PATH = "/home/sanse/ai-orchestrator/database/memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tool_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            tool_name TEXT,
            input TEXT,
            output TEXT,
            latency_ms REAL,
            success INTEGER,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            workflow_time_ms REAL,
            tool_invocations INTEGER,
            success INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_session() -> str:
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO sessions VALUES (?, ?, ?)", (session_id, now, now))
    conn.commit()
    conn.close()
    return session_id

def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (session_id, role, content, datetime.now().isoformat())
    )
    c.execute(
        "UPDATE sessions SET updated_at=? WHERE session_id=?",
        (datetime.now().isoformat(), session_id)
    )
    conn.commit()
    conn.close()

def get_history(session_id: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT role, content, timestamp FROM messages WHERE session_id=? ORDER BY id",
        (session_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows]

def save_tool_output(session_id: str, tool_name: str, input_data: str,
                     output: str, latency_ms: float, success: bool):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO tool_outputs (session_id, tool_name, input, output, latency_ms, success, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (session_id, tool_name, input_data, output, latency_ms, int(success), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def save_metrics(session_id: str, workflow_time_ms: float, tool_invocations: int, success: bool):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO metrics (session_id, workflow_time_ms, tool_invocations, success, timestamp) VALUES (?, ?, ?, ?, ?)",
        (session_id, workflow_time_ms, tool_invocations, int(success), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_metrics() -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    cols = ["id", "session_id", "workflow_time_ms", "tool_invocations", "success", "timestamp"]
    return [dict(zip(cols, r)) for r in rows]
