from fastapi import FastAPI, HTTPException  # FastAPI -> build the web endpoints and HTTPException-> throw web (404) errors
import requests # to make HTTP calls from our code to the local AI engine
from app.models.schemas import DocumentIngest, ChatQuery, ChatResponse
from app.db.vector_store import insert_document, search_documents

app = FastAPI(title="AI Memory Layer API", version="1.0.0")

# Local Ollama endpoint running on default port
OLLAMA_URL = "http://localhost:11434/api/generate"

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
@app.post("/chat", response_model=ChatResponse) # whatever this endpoint returns will match your strict ChatResponse format
async def chat_with_memory(query: ChatQuery): 
    """Retrieves relevant memory chunks and asks Ollama to generate an answer."""
    # 1. Retrieve context vectors (RAG)
    try:
        relevant_chunks = search_documents(query.query, top_k=query.top_k) # this returns the most textually relevant info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")  # throws error if retrieve was not successful

# Loops through the database search results and pastes them together into one large string block.
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

    # 3. Call local Ollama LLM
    ollama_payload = {
        "model": "qwen3.5:4b", # Change this to your downloaded model
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
