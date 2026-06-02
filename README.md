# AI Orchestration Framework

A modular AI workflow orchestration engine built with LangGraph, FastAPI, and SQLite. Accepts user queries, plans tasks, routes them to appropriate tools, maintains persistent memory, and returns synthesized responses through a graph-based workflow engine.

## Architecture
User Query → Planner Agent → Task Router → Tool Executor → Response Generator

Built as a directed graph using LangGraph:

- **Planner Agent** — Analyzes the query using Gemini LLM, determines required tools, and generates an execution plan
- **Task Router** — Dynamically routes tasks to the appropriate tool based on the plan
- **Tool Executor** — Runs tools and records latency, success/failure, and output to SQLite
- **Response Generator** — Synthesizes tool outputs into a final answer using Gemini

## Tools

| Tool | Description |
|------|-------------|
| RAG | Retrieves relevant documents using FAISS vector search and sentence-transformers embeddings |
| SQL | Executes analytical queries against the SQLite database |
| Calculator | Evaluates mathematical expressions using Python's math module |

## Tech Stack

- Python 3.10+
- LangGraph + LangChain
- FastAPI + Uvicorn
- SQLite (persistent memory)
- FAISS (vector search)
- Sentence Transformers (embeddings)
- Gemini API (LLM)

## Project Structure
ai-orchestrator/
├── api/
│   └── routes.py
├── agents/
│   ├── planner.py
│   ├── router.py
│   └── executor.py
├── tools/
│   ├── sql_tool.py
│   ├── rag_tool.py
│   └── calculator_tool.py
├── memory/
│   └── sqlite_store.py
├── workflows/
│   └── graph.py
├── database/
│   └── memory.db
├── app.py
├── requirements.txt
└── .env.example

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sanseet/ai-orchestrator.git
cd ai-orchestrator
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 4. Run the server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

### 5. Open API docs
http://localhost:8001/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/query` | Submit a query and run the full workflow |
| POST | `/session` | Create a new session |
| GET | `/history/{session_id}` | Retrieve conversation history |
| GET | `/metrics` | Get workflow execution metrics |
| GET | `/health` | Health check |

## Example Request

```bash
curl -X POST "http://localhost:8001/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantization in machine learning and calculate 2^10"}'
```

## Example Response

```json
{
  "session_id": "uuid-here",
  "query": "What is quantization in machine learning and calculate 2^10",
  "response": "Quantization reduces model size by converting FP32 weights to INT8. 2^10 = 1024.",
  "tools_used": ["rag", "calculator"],
  "plan": {
    "tools": ["rag", "calculator"],
    "plan": ["retrieve quantization info", "calculate 2^10"],
    "reasoning": "Query requires both knowledge retrieval and computation"
  }
}
```

## Observability

Every workflow execution tracks:
- Total workflow execution time (ms)
- Per-tool latency (ms)
- Tool success/failure status
- Number of tool invocations

All metrics stored in SQLite and accessible via GET /metrics.
