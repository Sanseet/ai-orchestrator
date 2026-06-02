import sqlite3
import logging
from typing import Any

logger = logging.getLogger(__name__)

DB_PATH = "/home/sanse/ai-orchestrator/database/memory.db"

class SQLTool:
    name = "sql"
    description = "Queries SQLite database for structured data"

    def run(self, query: str) -> str:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            cols = [d[0] for d in c.description] if c.description else []
            conn.close()
            if not rows:
                return "No results found."
            result = [dict(zip(cols, row)) for row in rows]
            logger.info(f"SQL tool executed: {query}")
            return str(result)
        except Exception as e:
            logger.error(f"SQL error: {e}")
            return f"Error: {str(e)}"
