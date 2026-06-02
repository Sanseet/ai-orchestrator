import math
import logging
from typing import Any

logger = logging.getLogger(__name__)

class CalculatorTool:
    name = "calculator"
    description = "Performs mathematical and statistical computations"

    def run(self, expression: str) -> str:
        try:
            allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
            allowed["abs"] = abs
            allowed["round"] = round
            result = eval(expression, {"__builtins__": {}}, allowed)
            logger.info(f"Calculator: {expression} = {result}")
            return str(result)
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return f"Error: {str(e)}"
