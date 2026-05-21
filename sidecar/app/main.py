from fastapi import FastAPI, HTTPException
import requests
from app.models.schemas import DocumentIngest, ChatQuery, ChatResponse
from app.db.vector_store import insert_document, search_documents

app = FastAPI(title="AI Memory Layer API", version="1.0.0")

# Local Ollama endpoint running on default port
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/ingest")
async def ingest_memory(doc: DocumentIngest):
    """Takes text, generates embeddings, and saves to LanceDB."""
    try:
        source = doc.metadata.get("source", "API")
        insert_document(doc.text, source)
        return {"status": "success", "message": "Document ingested into memory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_memory(query: ChatQuery):
    """Retrieves relevant memory chunks and asks Ollama to generate an answer."""
    # 1. Retrieve context vectors (RAG)
    try:
        relevant_chunks = search_documents(query.query, top_k=query.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    context_text = "\n\n".join([f"Source ({c['source']}): {c['text']}" for c in relevant_chunks])
    
    # 2. Build the prompt with retrieved context
    prompt = f"""
    You are an AI Memory Assistant. Use the following context to answer the user's question accurately.
    If the answer isn't in the context, say so. Do not hallucinate.

    CONTEXT:
    {context_text}

    QUESTION:
    {query.query}
    """

    # 3. Call local Ollama LLM (Assuming qwen2.5 or phi4 is pulled)
    ollama_payload = {
        "model": "qwen2.5", # Change this to your downloaded model
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=ollama_payload)
        response.raise_for_status()
        answer = response.json().get("response", "Could not generate an answer.")
        
        sources = list(set([c['source'] for c in relevant_chunks]))
        return ChatResponse(answer=answer, sources=sources)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Could not connect to local Ollama. Is the Ollama daemon running?")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
