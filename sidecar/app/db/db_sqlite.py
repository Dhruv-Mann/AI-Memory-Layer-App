import os
import sqlite3
import platform

def get_db_path() -> str:
    """
    Resolves the standardized local database storage path under the OS AppData folder.
    - Windows: %APPDATA%/ai-memory-layer
    - macOS: ~/Library/Application Support/ai-memory-layer
    - Linux: ~/.local/share/ai-memory-layer
    """
    if platform.system() == "Windows":
        app_data = os.environ.get("APPDATA")
    elif platform.system() == "Darwin":
        app_data = os.path.expanduser("~/Library/Application Support")
    else:
        app_data = os.path.expanduser("~/.local/share")
        
    db_dir = os.path.join(app_data, "ai-memory-layer")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "metadata.db")

def get_encryption_key() -> str:
    """
    Retrieves or generates a secure database key using the OS native keychain.
    Falls back gracefully to a hidden local file inside AppData if keyring is unavailable.
    """
    try:
        import keyring
        key = keyring.get_password("ai-memory-layer", "database_key")
        if not key:
            import secrets
            key = secrets.token_hex(32)
            keyring.set_password("ai-memory-layer", "database_key", key)
        return key
    except Exception:
        # Fallback to local hidden key file in the db folder
        app_data = os.path.dirname(get_db_path())
        key_file = os.path.join(app_data, ".key")
        if os.path.exists(key_file):
            with open(key_file, "r") as f:
                return f.read().strip()
        else:
            import secrets
            key = secrets.token_hex(32)
            with open(key_file, "w") as f:
                f.write(key)
            return key

def get_connection():
    """
    Establishes connection to the database. Attempts SQLCipher encryption, 
    falling back gracefully to standard SQLite standard library.
    """
    db_path = get_db_path()
    
    try:
        # Attempt to import SQLCipher bindings
        from pysqlcipher3 import dbapi2 as sqlite
        use_sqlcipher = True
    except ImportError:
        import sqlite3 as sqlite
        use_sqlcipher = False
        
    conn = sqlite.connect(db_path, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL")
    
    if use_sqlcipher:
        key = get_encryption_key()
        # Secure database access via SQLCipher key injection
        conn.execute(f"PRAGMA key = '{key}'")
        
    return conn

def initialize_database():
    """
    Initializes SQLite relational schema for tags, chunks, and FSRS scheduling logs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Topics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        mastery_score REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Chunks Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks_metadata (
        id TEXT PRIMARY KEY,
        file_path TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        file_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. FSRS Cards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fsrs_cards (
        id TEXT PRIMARY KEY,
        chunk_id TEXT NOT NULL,
        difficulty REAL DEFAULT 0.0,
        stability REAL DEFAULT 0.0,
        reps INTEGER DEFAULT 0,
        lapses INTEGER DEFAULT 0,
        state INTEGER DEFAULT 0, -- 0=New, 1=Learning, 2=Review, 3=Relearning
        last_review TIMESTAMP,
        next_review TIMESTAMP,
        FOREIGN KEY(chunk_id) REFERENCES chunks_metadata(id) ON DELETE CASCADE
    )
    """)
    
    # 4. FSRS Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fsrs_logs (
        id TEXT PRIMARY KEY,
        card_id TEXT NOT NULL,
        grade INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        state INTEGER NOT NULL,
        review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        interval INTEGER NOT NULL,
        FOREIGN KEY(card_id) REFERENCES fsrs_cards(id) ON DELETE CASCADE
    )
    """)
    
    # 5. Tags Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        type TEXT DEFAULT 'subject'
    )
    """)
    
    # 6. Chunk Tags Relation Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunk_tags (
        chunk_id TEXT NOT NULL,
        tag_id TEXT NOT NULL,
        PRIMARY KEY (chunk_id, tag_id),
        FOREIGN KEY(chunk_id) REFERENCES chunks_metadata(id) ON DELETE CASCADE,
        FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
    """)

    # 7. Embeddings Cache Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings_cache (
        text_hash TEXT PRIMARY KEY,
        vector TEXT NOT NULL, -- JSON string representation of list[float]
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def get_cached_embedding(text_hash: str):
    """
    Retrieves the cached vector list[float] for a given text hash, if present.
    """
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT vector FROM embeddings_cache WHERE text_hash = ?", (text_hash,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def cache_embedding(text_hash: str, vector: list):
    """
    Caches the generated vector list[float] mapped to its text hash.
    """
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO embeddings_cache (text_hash, vector) VALUES (?, ?)",
        (text_hash, json.dumps(vector))
    )
    conn.commit()
    conn.close()

def get_sources_matching_filters(tags: list = None, file_type: str = None) -> list:
    """
    Queries SQLite database to find file basenames matching specific tags and/or file types.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT DISTINCT file_path FROM chunks_metadata m"
    conditions = []
    params = []
    
    if file_type:
        conditions.append("m.file_type = ?")
        params.append(file_type)
        
    if tags:
        placeholders = ",".join(["?"] * len(tags))
        query += f" JOIN chunk_tags ct ON ct.chunk_id = m.id JOIN tags t ON t.id = ct.tag_id"
        conditions.append(f"t.name IN ({placeholders})")
        params.extend(tags)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    import os
    return [os.path.basename(r[0]) for r in rows]
