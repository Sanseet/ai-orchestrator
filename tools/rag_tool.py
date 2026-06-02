import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

logger = logging.getLogger(__name__)

DOCUMENTS = [
    "Qualcomm develops Snapdragon processors for mobile and edge AI.",
    "ONNX Runtime is a cross-platform inference engine for ML models.",
    "Quantization reduces model size by converting FP32 weights to INT8.",
    "LangGraph is a library for building stateful multi-agent workflows.",
    "FastAPI is a modern Python web framework for building REST APIs.",
    "SQLite is a lightweight embedded relational database.",
    "Edge computing brings computation closer to data sources.",
    "Neural networks consist of layers of interconnected nodes.",
    "Transformers use attention mechanisms for sequence modeling.",
    "Docker containers package applications with their dependencies.",
]

class RAGTool:
    name = "rag"
    description = "Retrieves relevant information from a knowledge base"

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = self.model.encode(DOCUMENTS)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype=np.float32))

    def run(self, query: str, top_k: int = 3) -> str:
        try:
            query_vec = self.model.encode([query])
            distances, indices = self.index.search(
                np.array(query_vec, dtype=np.float32), top_k
            )
            results = [DOCUMENTS[i] for i in indices[0]]
            logger.info(f"RAG retrieved {len(results)} documents for: {query}")
            return "\n".join(results)
        except Exception as e:
            logger.error(f"RAG error: {e}")
            return f"Error: {str(e)}"
