import logging
import os
from fastapi import FastAPI
from api.routes import router
from memory.sqlite_store import init_db
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(title="AI Orchestration Framework")
app.include_router(router)

@app.on_event("startup")
def startup():
    os.makedirs("/home/sanse/ai-orchestrator/database", exist_ok=True)
    init_db()
