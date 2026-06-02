import time
import logging
from typing import Any
from agents.router import TaskRouter
from memory.sqlite_store import save_tool_output

logger = logging.getLogger(__name__)

class ToolExecutor:
    def __init__(self):
        self.router = TaskRouter()

    def execute_sync(self, session_id: str, tool_name: str, input_data: str) -> dict:
        start = time.perf_counter()
        success = True
        try:
            result = self.router.route(tool_name, input_data)
        except Exception as e:
            result = f"Execution error: {str(e)}"
            success = False
            logger.error(f"Executor error for {tool_name}: {e}")

        latency_ms = (time.perf_counter() - start) * 1000
        save_tool_output(session_id, tool_name, input_data, result, latency_ms, success)
        return {"tool": tool_name, "result": result, "latency_ms": round(latency_ms, 2)}
