import logging
from typing import Any
from tools.calculator_tool import CalculatorTool
from tools.sql_tool import SQLTool
from tools.rag_tool import RAGTool

logger = logging.getLogger(__name__)

class TaskRouter:
    def __init__(self):
        self.tools = {
            "calculator": CalculatorTool(),
            "sql": SQLTool(),
            "rag": RAGTool(),
        }

    def route(self, tool_name: str, input_data: str) -> str:
        tool = self.tools.get(tool_name.strip().lower())
        if not tool:
            logger.warning(f"Tool not found: {tool_name}")
            return f"Tool '{tool_name}' not available."
        logger.info(f"Routing to tool: {tool_name}")
        return tool.run(input_data)
