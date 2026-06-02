import time
import logging
import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agents.planner import PlannerAgent
from agents.executor import ToolExecutor
from memory.sqlite_store import save_message, save_metrics
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

class WorkflowState(TypedDict):
    session_id: str
    query: str
    plan: dict
    tool_results: List[dict]
    final_response: str
    workflow_start: float

def plan_node(state: WorkflowState) -> WorkflowState:
    planner = PlannerAgent()
    plan = planner.plan(state["query"])
    logger.info(f"Plan: {plan}")
    return {**state, "plan": plan}

def execute_node(state: WorkflowState) -> WorkflowState:
    executor = ToolExecutor()
    results = []
    tools = state["plan"].get("tools", ["rag"])
    query = state["query"]
    for tool in tools:
        result = executor.execute_sync(state["session_id"], tool, query)
        results.append(result)
    return {**state, "tool_results": results}

def respond_node(state: WorkflowState) -> WorkflowState:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    tool_outputs = "\n".join([
        f"{r['tool']}: {r['result']}" for r in state["tool_results"]
    ])
    prompt = f"""Based on the following tool outputs, answer the user query.

Query: {state['query']}
Tool Outputs:
{tool_outputs}

Provide a clear, concise answer."""

    response = llm.invoke([HumanMessage(content=prompt)])
    final = response.content

    session_id = state["session_id"]
    save_message(session_id, "user", state["query"])
    save_message(session_id, "assistant", final)

    workflow_time = (time.perf_counter() - state["workflow_start"]) * 1000
    save_metrics(session_id, workflow_time, len(state["tool_results"]), True)

    return {**state, "final_response": final}

def build_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("planner", plan_node)
    graph.add_node("executor", execute_node)
    graph.add_node("responder", respond_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "responder")
    graph.add_edge("responder", END)
    return graph.compile()
