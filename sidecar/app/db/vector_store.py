import os
import uuid
import hashlib
import lancedb
import pyarrow as pa
from typing import List, Dict, Any

from app.ml.embeddings import generate_embedding
from app.ml.parsers import parse_file
from app.ml.chunking import chunk_document
from app.db.db_sqlite import get_connection

# We store the vector DB inside the local app data or workspace to remain 100% local
DB_PATH = os.path.join(os.path.dirname(__file__), "../../../local_data/lancedb")

# Define the schema for LanceDB (256-dimensions using Matryoshka nomic-embed)
schema = pa.schema([
    pa.field("vector", pa.list_(pa.float32(), 256)),
    pa.field("text", pa.string()),
    pa.field("source", pa.string())
])

def get_table():
    db = lancedb.connect(DB_PATH)
    if "memory_chunks" not in db.table_names():
        return db.create_table("memory_chunks", schema=schema)
    return db.open_table("memory_chunks")

def insert_document(text: str, source: str = "manual") -> bool:
    """
    Generates embedding for a standalone text string and inserts it into LanceDB.
    """
    table = get_table()
    vector = generate_embedding(text)
    table.add([{
        "vector": vector,
        "text": text,
        "source": source
    }])
    return True

def search_documents(query: str, top_k: int = 3) -> List[dict]:
    """
    Performs vector similarity search in LanceDB and returns the most relevant chunks.
    """
    table = get_table()
    query_vector = generate_embedding(query)
    results = table.search(query_vector).limit(top_k).to_list()
    return results

def ingest_file_to_store(file_path: str, tags: List[str] = None) -> bool:
    """
    Robust pipeline to:
    1. Parse a file (Markdown, PDF, or code) extracting text content and metadata
    2. Check for redundant processing using SHA-256 hashes (updating existing indexes if modified)
    3. Slice text into syntax-aware code blocks or prose chunks
    4. Compute 256-dimension embeddings and cache them
    5. Batch store vector chunks in LanceDB
    6. Register relational FSRS tracking metadata and tag mappings in SQLite
    """
    # 1. Parse File
    content, metadata = parse_file(file_path)
    if not content.strip():
        return False
        
    file_type = metadata.get("type", "text")
    language = metadata.get("language", "text")
    source = metadata.get("source", os.path.basename(file_path))
    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if identical file was already indexed
    cursor.execute("SELECT id FROM chunks_metadata WHERE file_path = ? AND file_hash = ?", (file_path, file_hash))
    exists = cursor.fetchone()
    if exists:
        conn.close()
        return True
        
    # If the file exists but has changed (hash mismatch), clear the old indexes first
    cursor.execute("SELECT id FROM chunks_metadata WHERE file_path = ?", (file_path,))
    old_record = cursor.fetchone()
    if old_record:
        old_id = old_record[0]
        # Clean up relational records
        cursor.execute("DELETE FROM chunks_metadata WHERE id = ?", (old_id,))
        # Clear vector entries
        table = get_table()
        table.delete(f"source = '{source}'")
        
    conn.commit()
    conn.close()
        
    file_record_id = str(uuid.uuid4())
    
    # 2. Chunk Content
    chunks = chunk_document(content, language=language)
    
    # 3. Embed Chunks (does its own connection handling internally)
    rows_to_add = []
    card_records = []
    
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{file_record_id}_{idx}"
        vector = generate_embedding(chunk)
        
        rows_to_add.append({
            "vector": vector,
            "text": chunk,
            "source": source
        })
        card_records.append((chunk_id, file_record_id))
        
    if rows_to_add:
        table = get_table()
        table.add(rows_to_add)
        
    # 4. Save metadata, FSRS cards, and tags in a single fast transaction
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert new file record
    cursor.execute(
        "INSERT INTO chunks_metadata (id, file_path, file_hash, file_type) VALUES (?, ?, ?, ?)",
        (file_record_id, file_path, file_hash, file_type)
    )
    
    # Batch insert cards
    cursor.executemany(
        "INSERT INTO fsrs_cards (id, chunk_id, difficulty, stability, reps, lapses, state) VALUES (?, ?, 0.0, 0.0, 0, 0, 0)",
        card_records
    )
    
    # Handle Tags
    file_tags = tags or []
    if "tags" in metadata and isinstance(metadata["tags"], list):
        file_tags.extend(metadata["tags"])
        
    for t_name in set(file_tags):
        t_id = hashlib.md5(t_name.lower().strip().encode("utf-8")).hexdigest()
        cursor.execute("INSERT OR IGNORE INTO tags (id, name, type) VALUES (?, ?, ?)", (t_id, t_name.strip(), "subject"))
        cursor.execute("INSERT OR IGNORE INTO chunk_tags (chunk_id, tag_id) VALUES (?, ?)", (file_record_id, t_id))
        
    conn.commit()
    conn.close()
    return True

def hybrid_search(query: str, tags: List[str] = None, file_type: str = None, top_k: int = 5) -> List[dict]:
    """
    Performs hybrid search combining vector similarity and FTS keyword search,
    scoring results using Reciprocal Rank Fusion (RRF), bounded by SQLite metadata filters.
    """
    from app.db.db_sqlite import get_sources_matching_filters
    table = get_table()
    
    # 1. Resolve SQLite metadata filters
    sources = None
    if tags or file_type:
        sources = get_sources_matching_filters(tags, file_type)
        if not sources:
            return [] # No files match metadata filters
            
    # Prepare filter condition for LanceDB
    filter_expr = None
    if sources is not None:
        escaped_sources = [s.replace("'", "''") for s in sources]
        filter_expr = f"source IN ({','.join([f'\'{s}\'' for s in escaped_sources])})"
        
    # 2. Vector similarity search
    query_vector = generate_embedding(query)
    vec_query = table.search(query_vector)
    if filter_expr:
        vec_query = vec_query.where(filter_expr)
    vec_results = vec_query.limit(top_k * 2).to_list()
    
    # 3. Full-Text keyword search
    fts_results = []
    try:
        try:
            table.create_fts_index("text", replace=False)
        except Exception:
            pass
            
        fts_query = table.search(query)
        if filter_expr:
            fts_query = fts_query.where(filter_expr)
        fts_results = fts_query.limit(top_k * 2).to_list()
    except Exception as e:
        print(f"FTS search fallback triggered: {e}")
        fts_results = []
        
    # 4. Reciprocal Rank Fusion (RRF)
    rrf_scores = {}
    doc_map = {}
    constant = 60
    
    for rank, doc in enumerate(vec_results):
        doc_id = doc["text"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (constant + rank + 1))
        
    for rank, doc in enumerate(fts_results):
        doc_id = doc["text"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (constant + rank + 1))
        
    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    final_results = []
    for doc_id, score in sorted_docs[:top_k]:
        final_results.append(doc_map[doc_id])
        
    return final_results
