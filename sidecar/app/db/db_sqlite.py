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

def get_due_cards(limit: int = 20) -> list:
    """
    Retrieves due cards from SQLite, merges their actual text content from LanceDB,
    and returns Svelte-compatible review models.
    """
    import os
    from app.db.vector_store import get_table
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        c.id, c.chunk_id, m.file_path, m.file_type, 
        c.difficulty, c.stability, c.reps, c.lapses, c.state, 
        c.last_review, c.next_review,
        (SELECT GROUP_CONCAT(t.name) FROM chunk_tags ct JOIN tags t ON t.id = ct.tag_id WHERE ct.chunk_id = m.id) as tags
    FROM fsrs_cards c
    JOIN chunks_metadata m ON m.id = c.chunk_id
    WHERE c.next_review IS NULL OR c.next_review <= datetime('now')
    ORDER BY 
        CASE WHEN c.next_review IS NULL THEN 1 ELSE 0 END,
        c.next_review ASC
    LIMIT ?
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    table = get_table()
    due_cards = []
    
    for row in rows:
        card_id, chunk_id, file_path, file_type, difficulty, stability, reps, lapses, state, last_review, next_review, tags_str = row
        
        text = ""
        source = os.path.basename(file_path)
        try:
            chunk_results = table.search().where(f"chunk_id = '{card_id}'").limit(1).to_list()
            if chunk_results:
                text = chunk_results[0]["text"]
                source = chunk_results[0]["source"]
            else:
                continue
        except Exception as e:
            print(f"Error fetching LanceDB chunk text for card {card_id}: {e}")
            continue
            
        due_cards.append({
            "id": card_id,
            "chunk_id": chunk_id,
            "text": text,
            "source": source,
            "file_path": file_path,
            "file_type": file_type,
            "difficulty": difficulty,
            "stability": stability,
            "reps": reps,
            "lapses": lapses,
            "state": state,
            "last_review": last_review,
            "next_review": next_review,
            "tags": tags_str.split(",") if tags_str else []
        })
        
    return due_cards

def rate_card(card_id: str, grade: int) -> dict:
    """
    Applies the FSRS-5 scheduling algorithm to a review card, updates SQLite tables
    (fsrs_cards and fsrs_logs), and returns the updated card details.
    """
    from app.ml.fsrs import FSRS
    import uuid
    from datetime import datetime, timedelta
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT chunk_id, difficulty, stability, reps, lapses, state, last_review FROM fsrs_cards WHERE id = ?",
        (card_id,)
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError(f"Card {card_id} not found.")
        
    chunk_id, difficulty, stability, reps, lapses, state, last_review = row
    
    elapsed_days = 0
    if last_review:
        try:
            last_dt = datetime.strptime(last_review, "%Y-%m-%d %H:%M:%S")
            elapsed_days = max(0, (datetime.now() - last_dt).days)
        except Exception:
            pass
            
    fsrs = FSRS()
    new_s, new_d, interval = fsrs.step(stability, difficulty, reps, lapses, grade, elapsed_days)
    
    if grade == 1:
        new_state = 3 # Relearning
        new_lapses = lapses + 1
    else:
        new_state = 2 # Review
        new_lapses = lapses
        
    new_reps = reps + 1
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    next_review_dt = datetime.now() + timedelta(days=interval)
    next_review_str = next_review_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        """
        UPDATE fsrs_cards
        SET difficulty = ?, stability = ?, reps = ?, lapses = ?, state = ?, last_review = ?, next_review = ?
        WHERE id = ?
        """,
        (new_d, new_s, new_reps, new_lapses, new_state, now_str, next_review_str, card_id)
    )
    
    log_id = str(uuid.uuid4())
    cursor.execute(
        """
        INSERT INTO fsrs_logs (id, card_id, grade, rating, state, interval, review_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (log_id, card_id, grade, grade, new_state, interval, now_str)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "id": card_id,
        "difficulty": new_d,
        "stability": new_s,
        "reps": new_reps,
        "lapses": new_lapses,
        "state": new_state,
        "last_review": now_str,
        "next_review": next_review_str,
        "interval_days": interval
    }

def get_mastery_analytics() -> dict:
    """
    Computes weak-topic detection, mastery scores, daily review heatmap activity,
    and predicted knowledge decay curves per tag.
    """
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM tags")
    tags = cursor.fetchall()
    
    tag_mastery = []
    decay_curves = {}
    
    for tag_id, tag_name in tags:
        cursor.execute(
            """
            SELECT c.stability, c.last_review, c.reps, c.lapses
            FROM fsrs_cards c
            JOIN chunk_tags ct ON ct.chunk_id = c.chunk_id
            WHERE ct.tag_id = ?
            """,
            (tag_id,)
        )
        cards = cursor.fetchall()
        
        if not cards:
            continue
            
        r_sum = 0.0
        active_count = 0
        
        for stability, last_review, reps, lapses in cards:
            if reps > 0 and last_review:
                try:
                    last_dt = datetime.strptime(last_review, "%Y-%m-%d %H:%M:%S")
                    elapsed = max(0, (datetime.now() - last_dt).days)
                    r = (1.0 + elapsed / (9.0 * stability)) ** -0.5
                    r_sum += r
                    active_count += 1
                except Exception:
                    pass
                    
        mastery = (r_sum / active_count) if active_count > 0 else 1.0
        
        cursor.execute(
            """
            SELECT COUNT(*), SUM(CASE WHEN l.grade > 1 THEN 1 ELSE 0 END)
            FROM fsrs_logs l
            JOIN fsrs_cards c ON c.id = l.card_id
            JOIN chunk_tags ct ON ct.chunk_id = c.chunk_id
            WHERE ct.tag_id = ?
            """,
            (tag_id,)
        )
        log_counts = cursor.fetchone()
        total_logs = log_counts[0] if log_counts else 0
        success_logs = log_counts[1] if log_counts and log_counts[1] is not None else 0
        accuracy = (success_logs / total_logs) if total_logs > 0 else 1.0
        
        tag_mastery.append({
            "tag": tag_name,
            "mastery_score": round(mastery * 100, 1),
            "accuracy": round(accuracy * 100, 1),
            "total_reviews": total_logs,
            "card_count": len(cards)
        })
        
        decay_curve = []
        for day in range(30):
            r_day_sum = 0.0
            card_count_for_decay = 0
            for stability, last_review, reps, lapses in cards:
                if reps > 0 and last_review:
                    try:
                        last_dt = datetime.strptime(last_review, "%Y-%m-%d %H:%M:%S")
                        elapsed = max(0, (datetime.now() - last_dt).days) + day
                        r_day = (1.0 + elapsed / (9.0 * stability)) ** -0.5
                        r_day_sum += r_day
                        card_count_for_decay += 1
                    except Exception:
                        pass
            avg_r_day = (r_day_sum / card_count_for_decay) if card_count_for_decay > 0 else 1.0
            decay_curve.append(round(avg_r_day * 100, 1))
            
        decay_curves[tag_name] = decay_curve
        
    cursor.execute(
        """
        SELECT date(review_time) as rev_date, count(*) as count
        FROM fsrs_logs
        WHERE review_time >= datetime('now', '-90 days')
        GROUP BY rev_date
        ORDER BY rev_date ASC
        """
    )
    heatmap_rows = cursor.fetchall()
    heatmap = {r[0]: r[1] for r in heatmap_rows}
    
    conn.close()
    
    return {
        "tag_mastery": tag_mastery,
        "decay_curves": decay_curves,
        "heatmap": heatmap
    }
