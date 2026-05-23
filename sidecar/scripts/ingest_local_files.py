import sys
import os
import time

# Ensure Python can find the 'app' module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.ml.chunking import chunk_document
from app.db.vector_store import insert_document

def ingest_markdown_file(file_path: str):
    print(f"Reading file: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 1: Chunk the massive file
    chunks = chunk_document(content, chunk_size=1000)
    print(f"File sliced into {len(chunks)} contextual chunks (with 15% overlap).")
    
    filename = os.path.basename(file_path)
    
    # Step 2: Ingest each chunk into LanceDB
    print("Ingesting chunks to LanceDB (Converting to Vectors)...")
    for i, chunk_text in enumerate(chunks):
        # We append a tag so the AI knows exactly which file AND which section this is
        source_tag = f"{filename} (Chunk {i+1}/{len(chunks)})"
        insert_document(chunk_text, source=source_tag)
        
    print(f"Successfully processed and memorized: {filename}\n")

if __name__ == "__main__":
    # Let's target the core local knowledge files sitting in the root of the workspace
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    
    files_to_ingest = [
        "PROJECT_BRAIN.md",
        "AI_Memory_Layer_Context.md"
    ]
    
    for md_file in files_to_ingest:
        full_path = os.path.join(workspace_root, md_file)
        if os.path.exists(full_path):
            ingest_markdown_file(full_path)
        else:
            print(f"Could not find {md_file} at {full_path}")
