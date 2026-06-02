import time
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from memory.sqlite_store import create_session, get_history, get_metrics
from workflows.graph import build_graph

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    session_id: str = None

@router.post("/query")
async def run_query(request: QueryRequest):
    session_id = request.session_id or create_session()
    graph = build_graph()
    state = {
        "session_id": session_id,
        "query": request.query,
        "plan": {},
        "tool_results": [],
        "final_response": "",
        "workflow_start": time.perf_counter()
    }
    try:
        result = graph.invoke(state)
        return {
            "session_id": session_id,
            "query": request.query,
            "response": result["final_response"],
            "tools_used": [r["tool"] for r in result["tool_results"]],
            "plan": result["plan"]
        }
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session")
def create_new_session():
    session_id = create_session()
    return {"session_id": session_id}

@router.get("/history/{session_id}")
def get_session_history(session_id: str):
    history = get_history(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": history}

@router.get("/metrics")
def get_all_metrics():
    return {"metrics": get_metrics()}

@router.get("/health")
def health():
    return {"status": "healthy"}
