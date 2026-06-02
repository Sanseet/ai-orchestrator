import logging
from typing import Any
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

class PlannerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def plan(self, query: str) -> dict:
        prompt = f"""You are a task planner. Given a user query, determine:
1. What tools are needed (choose from: calculator, sql, rag)
2. What subtasks to execute
3. The execution order

Query: {query}

Respond in this exact format:
TOOLS: tool1,tool2
PLAN: step1 | step2 | step3
REASONING: brief explanation"""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            text = response.content
            logger.info(f"Planner response: {text}")

            tools = []
            plan = []
            reasoning = ""

            for line in text.split("\n"):
                if line.startswith("TOOLS:"):
                    tools = [t.strip() for t in line.replace("TOOLS:", "").split(",")]
                elif line.startswith("PLAN:"):
                    plan = [s.strip() for s in line.replace("PLAN:", "").split("|")]
                elif line.startswith("REASONING:"):
                    reasoning = line.replace("REASONING:", "").strip()

            return {"tools": tools, "plan": plan, "reasoning": reasoning}
        except Exception as e:
            logger.error(f"Planner error: {e}")
            return {"tools": ["rag"], "plan": [query], "reasoning": "fallback"}
