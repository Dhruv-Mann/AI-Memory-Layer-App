from fastapi import FastAPI, HTTPException, Request, UploadFile, File
import requests # to make HTTP calls from our code to the local AI engine
import os
from app.models.schemas import DocumentIngest, ChatQuery, ChatResponse, GradeRequest
from app.db.vector_store import insert_document, search_documents

from fastapi.responses import JSONResponse
import logging

# Configure basic logging to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="AI Memory Layer API", version="1.0.0")

# Local Ollama endpoint running on default port
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing metadata databases and tables...")
    from app.db.db_sqlite import initialize_database
    initialize_database()
    logger.info("Metadata databases initialized successfully.")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": f"An unexpected error occurred: {str(exc)}"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail}
    )

@app.get("/")
async def root():
    return {"message": "AI Memory Layer API is running. Go to /docs to test the endpoints!"}

@app.post("/ingest")  # This is a 'POST' network route which is used to save new docs or notes into the local AI memory 
async def ingest_memory(doc: DocumentIngest): # It expects incoming data to strictly match the DocumentIngest format
    """Takes text, generates embeddings, and saves to LanceDB."""
    try:
        source = doc.metadata.get("source", "API") # looks inside the metadata dict for a 'source' value. If not provided then it
                                                   # defaults to label it as 'API'.
        insert_document(doc.text, source) # Hands over the data to LanceDB storage script to create the mathematical embeddings and save
                                          # it in the hard drive.

        return {"status": "success", "message": "Document ingested into memory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # throw error if insertion was unsuccessful

# this implements the RAG loop
@app.post("/chat", response_model=ChatResponse)
async def chat_with_memory(query: ChatQuery): 
    """Retrieves relevant memory chunks via hybrid search, reranks them, and queries Ollama."""
    print(f"\n--- New Chat Request Received ---")
    print(f"User Query: {query.query}")
    
    # 1. Retrieve candidates via Hybrid Search
    try:
        from app.db.vector_store import hybrid_search
        print("Searching databases with hybrid vector + FTS index...")
        # Get twice top_k candidates for the reranker to work with
        candidates = hybrid_search(
            query=query.query,
            tags=query.tags,
            file_type=query.file_type,
            top_k=query.top_k * 2
        )
        print(f"Found {len(candidates)} hybrid candidates.")
    except Exception as e:
        print(f"Database Search Error: {e}")
        raise HTTPException(status_code=500, detail=f"Database search error: {str(e)}")

    # 2. Cross-Encoder Reranking
    try:
        from app.ml.reranker import rerank_chunks
        print("Reranking candidates with Cross-Encoder...")
        relevant_chunks = rerank_chunks(query.query, candidates, top_k=query.top_k)
        print(f"Reranked down to top {len(relevant_chunks)} chunks.")
    except Exception as e:
        print(f"Reranker Error: {e}. Falling back to default candidates.")
        relevant_chunks = candidates[:query.top_k]

    # Form context text block
    context_text = "\n\n".join([f"Source ({c['source']}): {c['text']}" for c in relevant_chunks]) 
    
    # 3. Assemble prompt
    prompt = f"""
    You are an AI Memory Assistant. Use the following context to answer the user's question accurately.
    If the answer isn't in the context, say so. Do not hallucinate.

    CONTEXT:
    {context_text}

    QUESTION:
    {query.query}
    """

    # 4. Call local Ollama LLM with Keep-Alive parameter (unload after 5 minutes of inactivity)
    selected_model = query.model or "qwen3.5:4b"
    ollama_payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "keep_alive": "5m" # Unloads LLM from memory after 5 minutes of idle time
        }
    }

    try:
        print(f"Sending prompt to Ollama ({selected_model}) with 5-minute keep_alive...")
        response = requests.post(OLLAMA_URL, json=ollama_payload)
        response.raise_for_status()
        
        answer = response.json().get("response", "Could not generate an answer.")
        print("Ollama successfully generated an answer!")
        
        sources = list(set([c['source'] for c in relevant_chunks]))
        return ChatResponse(answer=answer, sources=sources)
    except requests.exceptions.RequestException as e:
        print(f"Ollama Error: {e}")
        raise HTTPException(status_code=503, detail="Could not connect to local Ollama. Is the Ollama daemon running?")

@app.get("/review/due")
async def get_due_items(limit: int = 20):
    """
    Returns the current queue of cards due for FSRS review.
    """
    try:
        from app.db.db_sqlite import get_due_cards
        due_cards = get_due_cards(limit=limit)
        return due_cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/grade")
async def submit_review_grade(request: GradeRequest):
    """
    Submits a review grade (1-4) for a card, updating stability/difficulty metrics.
    """
    if request.grade not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Grade must be between 1 and 4.")
    try:
        from app.db.db_sqlite import rate_card
        result = rate_card(request.card_id, request.grade)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """
    Calculates and returns tag mastery, decay curves, and heatmap stats.
    """
    try:
        from app.db.db_sqlite import get_mastery_analytics
        analytics = get_mastery_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workspace/export")
async def export_workspace():
    """
    Compiles database and LanceDB vector files into a ZIP archive for backup.
    """
    import zipfile
    import tempfile
    from fastapi.responses import FileResponse
    from app.db.db_sqlite import get_db_path
    from app.db.vector_store import DB_PATH
    
    try:
        temp_dir = tempfile.gettempdir()
        zip_path = os.path.join(temp_dir, "ai-memory-workspace.zip")
        
        sqlite_path = get_db_path()
        lancedb_dir = DB_PATH
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(sqlite_path):
                zipf.write(sqlite_path, "metadata.db")
                
            if os.path.exists(lancedb_dir):
                for root, dirs, files in os.walk(lancedb_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.join(lancedb_dir, ".."))
                        zipf.write(file_path, arcname)
                        
        return FileResponse(zip_path, media_type="application/zip", filename="ai-memory-workspace.zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.post("/workspace/import")
async def import_workspace(file: UploadFile = File(...)):
    """
    Restores database and vector files from a compiled backup ZIP.
    """
    import zipfile
    import tempfile
    import shutil
    from app.db.db_sqlite import get_db_path
    from app.db.vector_store import DB_PATH
    
    try:
        temp_dir = tempfile.gettempdir()
        zip_path = os.path.join(temp_dir, "imported-workspace.zip")
        
        with open(zip_path, "wb") as f:
            f.write(await file.read())
            
        sqlite_path = get_db_path()
        lancedb_dir = DB_PATH
        
        # Overwrite: clean current lancedb if it exists
        shutil.rmtree(lancedb_dir, ignore_errors=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            for member in zipf.infolist():
                if member.filename == "metadata.db":
                    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
                    with zipf.open(member) as source, open(sqlite_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                elif member.filename.startswith("lancedb/"):
                    target_dir = os.path.dirname(lancedb_dir)
                    zipf.extract(member, path=target_dir)
                    
        return {"status": "success", "message": "Workspace imported and restored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Simple port resolution parameter
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
            
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)
