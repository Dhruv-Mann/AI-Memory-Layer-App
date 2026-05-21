import os
import lancedb
import pyarrow as pa
from typing import List
from app.ml.embeddings import generate_embedding

# We store the vector DB inside the local app data or workspace to remain 100% local
DB_PATH = os.path.join(os.path.dirname(__file__), "../../../local_data/lancedb")

# Define the schema for LanceDB
schema = pa.schema([
    pa.field("vector", pa.list_(pa.float32(), 768)), # 768 dimensions for nomic-embed-text
    pa.field("text", pa.string()),
    pa.field("source", pa.string())
])

def get_table():
    db = lancedb.connect(DB_PATH)
    if "memory_chunks" not in db.table_names():
        return db.create_table("memory_chunks", schema=schema)
    return db.open_table("memory_chunks")

def insert_document(text: str, source: str = "manual"):
    table = get_table()
    vector = generate_embedding(text)
    
    # Store the single text chunk with its vector and metadata
    table.add([{
        "vector": vector,
        "text": text,
        "source": source
    }])
    return True

def search_documents(query: str, top_k: int = 3) -> List[dict]:
    table = get_table()
    query_vector = generate_embedding(query)
    
    # Perform vector similarity search
    results = table.search(query_vector).limit(top_k).to_list()
    return results
