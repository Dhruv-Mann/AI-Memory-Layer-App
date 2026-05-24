import pytest
import os
import shutil
import tempfile
from _pytest.monkeypatch import MonkeyPatch

@pytest.fixture(scope="session", autouse=True)
def mock_db_paths():
    """
    Redirects both SQLite and LanceDB databases to a temporary directory 
    for isolated unit and integration testing.
    """
    mp = MonkeyPatch()
    temp_dir = tempfile.mkdtemp()
    
    # SQLite Override
    test_db_path = os.path.join(temp_dir, "test_metadata.db")
    import app.db.db_sqlite as db_sqlite
    mp.setattr(db_sqlite, "get_db_path", lambda: test_db_path)
    
    # LanceDB Override
    test_lancedb_dir = os.path.join(temp_dir, "test_lancedb")
    import app.db.vector_store as vector_store
    mp.setattr(vector_store, "DB_PATH", test_lancedb_dir)
    
    # Ensure fresh schema initialized
    db_sqlite.initialize_database()
    
    yield
    
    mp.undo()
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def clean_db():
    """
    Helper fixture to clear out SQLite rows and LanceDB chunks between tests.
    """
    import app.db.db_sqlite as db_sqlite
    import app.db.vector_store as vector_store
    
    conn = db_sqlite.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fsrs_logs")
    cursor.execute("DELETE FROM fsrs_cards")
    cursor.execute("DELETE FROM chunk_tags")
    cursor.execute("DELETE FROM chunks_metadata")
    cursor.execute("DELETE FROM tags")
    cursor.execute("DELETE FROM topics")
    conn.commit()
    conn.close()
    
    # LanceDB recreate table
    try:
        table = vector_store.get_table()
        # To clear, we can delete all elements if table has data, or just clean directory
        # The simplest way is to drop the table and recreate it
        db = vector_store.lancedb.connect(vector_store.DB_PATH)
        if "memory_chunks" in db.table_names():
            db.drop_table("memory_chunks")
    except Exception:
        pass
        
    yield
