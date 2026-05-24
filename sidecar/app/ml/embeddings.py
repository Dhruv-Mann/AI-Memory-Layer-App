import os
import time
import hashlib
from sentence_transformers import SentenceTransformer
import numpy as np
from app.db.db_sqlite import get_cached_embedding, cache_embedding

print("Initializing Embedding Engine...")
try:
    # Use SentenceTransformer. It automatically downloads/caches weights locally.
    EMBEDDING_MODEL = SentenceTransformer("nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True)
    use_sentence_transformers = True
except Exception as e:
    print(f"Warning: Failed to load SentenceTransformer: {e}. Attempting ONNX fallback.")
    use_sentence_transformers = False

class ONNXEmbeddingEngine:
    """
    Self-contained ONNX Inference Session runner for CPU-optimized embedding generation.
    Supports thread allocations and graph optimizations.
    """
    def __init__(self, model_dir: str):
        import onnxruntime as ort
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        
        # CPU Optimizations for local execution
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4
        opts.inter_op_num_threads = 4
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        model_path = os.path.join(model_dir, "model.onnx")
        self.session = ort.InferenceSession(model_path, sess_options=opts, providers=["CPUExecutionProvider"])

    def encode(self, text: str) -> list[float]:
        # Encode inputs
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=8192, return_tensors="np")
        onnx_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64)
        }
        if "token_type_ids" in inputs:
            onnx_inputs["token_type_ids"] = inputs["token_type_ids"].astype(np.int64)
            
        outputs = self.session.run(None, onnx_inputs)
        embeddings = outputs[0]
        
        # Mean pooling
        attention_mask = inputs["attention_mask"]
        input_mask_expanded = np.expand_dims(attention_mask, -1).astype(float)
        sum_embeddings = np.sum(embeddings * input_mask_expanded, 1)
        sum_mask = np.clip(input_mask_expanded.sum(1), a_min=1e-9, a_max=None)
        mean_pooled = sum_embeddings / sum_mask
        
        # L2 normalization
        norm = np.linalg.norm(mean_pooled, axis=1, keepdims=True)
        normalized = mean_pooled / np.clip(norm, a_min=1e-9, a_max=None)
        
        # Matryoshka dimension truncation (256 dimensions)
        truncated = normalized[0][:256]
        # Re-normalize vector after truncation
        trunc_norm = np.linalg.norm(truncated)
        final_vector = (truncated / np.clip(trunc_norm, a_min=1e-9, a_max=None)).tolist()
        
        return final_vector

def compute_text_hash(text: str) -> str:
    """
    Computes SHA-256 hash of text for caching.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def generate_embedding(text: str) -> list[float]:
    """
    Generates embedding vector (256-dimensional) for a given text segment.
    Checks the local SQLite database cache first to prevent redundant inferences.
    """
    text_hash = compute_text_hash(text)
    
    # 1. Check local cache
    cached_vector = get_cached_embedding(text_hash)
    if cached_vector is not None:
        return cached_vector
        
    start_time = time.time()
    
    # 2. Perform Inference
    if use_sentence_transformers:
        # Generate full embedding (768 dimensions)
        vector_full = EMBEDDING_MODEL.encode(text)
        # Matryoshka dimension truncation to 256
        vector_trunc = vector_full[:256]
        # Re-normalize vector after truncation
        norm = np.linalg.norm(vector_trunc)
        vector = (vector_trunc / np.clip(norm, a_min=1e-9, a_max=None)).tolist()
    else:
        # Fallback to local ONNX model if configured
        import platform
        if platform.system() == "Windows":
            app_data = os.environ.get("APPDATA")
        elif platform.system() == "Darwin":
            app_data = os.path.expanduser("~/Library/Application Support")
        else:
            app_data = os.path.expanduser("~/.local/share")
        model_dir = os.path.join(app_data, "ai-memory-layer", "models", "nomic-embed")
        engine = ONNXEmbeddingEngine(model_dir)
        vector = engine.encode(text)

    end_time = time.time()
    
    # 3. Cache the newly computed embedding
    cache_embedding(text_hash, vector)
    
    print(f"Generated embedding. Dimensions: {len(vector)}. Time: {round(end_time - start_time, 3)}s.")
    return vector

if __name__ == "__main__":
    # Initialize DB for standalone test execution
    from app.db.db_sqlite import initialize_database
    initialize_database()
    
    sample_text = "Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems."
    generate_embedding(sample_text)
