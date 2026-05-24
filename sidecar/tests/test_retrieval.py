import pytest
import os
import tempfile
from app.db.vector_store import insert_document, search_documents, hybrid_search, ingest_file_to_store
from app.db.db_sqlite import get_connection

def test_vector_insertion_and_search(clean_db):
    # Test insertion
    assert insert_document("Artificial Intelligence and Machine Learning represent the future.", "test_src")
    
    # Test similarity search
    results = search_documents("Machine Learning", top_k=1)
    assert len(results) == 1
    assert "Artificial Intelligence" in results[0]["text"]
    assert results[0]["source"] == "test_src"

def test_hybrid_search(clean_db):
    insert_document("Deep learning model architectures.", "test_deep")
    insert_document("Traditional linear programming algorithms.", "test_linear")
    
    # Search for "Deep learning"
    results = hybrid_search("Deep learning", top_k=2)
    assert len(results) >= 1
    assert "Deep learning" in results[0]["text"]

def test_ingest_file_to_store(clean_db):
    markdown_content = """---
tags: [science, programming]
---
# Python Programming
Python is a multi-paradigm programming language.
"""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        f.write(markdown_content)
        temp_path = f.name
        
    try:
        # Ingest file
        success = ingest_file_to_store(temp_path, tags=["manual-tag"])
        assert success
        
        # Verify SQLite entries
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verify file record in chunks_metadata
        cursor.execute("SELECT file_path, file_type FROM chunks_metadata")
        row = cursor.fetchone()
        assert row is not None
        assert row[1] == "markdown"
        
        # Verify cards created in fsrs_cards
        cursor.execute("SELECT COUNT(*) FROM fsrs_cards")
        count = cursor.fetchone()[0]
        assert count > 0
        
        # Verify tags
        cursor.execute("SELECT name FROM tags")
        tags = [r[0] for r in cursor.fetchall()]
        assert "science" in tags
        assert "programming" in tags
        assert "manual-tag" in tags
        
        conn.close()
        
        # Verify LanceDB search returns the chunk
        results = search_documents("Python Programming", top_k=1)
        assert len(results) == 1
        assert "Python" in results[0]["text"]
        
    finally:
        os.remove(temp_path)
