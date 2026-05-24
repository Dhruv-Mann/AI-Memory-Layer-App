from sentence_transformers import CrossEncoder

CROSS_ENCODER = None

def get_cross_encoder():
    """
    Lazily instantiates the lightweight cross-encoder model to save boot memory.
    """
    global CROSS_ENCODER
    if CROSS_ENCODER is None:
        try:
            # Extremely light and fast reranker model optimized for CPU
            CROSS_ENCODER = CrossEncoder("mixedbread-ai/mxbai-rerank-xsmall-v1")
        except Exception as e:
            print(f"Warning: Failed to load CrossEncoder reranker: {e}")
    return CROSS_ENCODER

def rerank_chunks(query: str, chunks: list[dict], top_k: int = 3) -> list[dict]:
    """
    Reranks candidate retrieved chunks using a local Cross-Encoder.
    Returns the top K highest relevance chunks.
    """
    model = get_cross_encoder()
    if not model or not chunks:
        return chunks[:top_k]
        
    pairs = [(query, c["text"]) for c in chunks]
    try:
        scores = model.predict(pairs)
        scored_chunks = list(zip(chunks, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in scored_chunks[:top_k]]
    except Exception as e:
        print(f"Reranking error: {e}. Falling back to default order.")
        return chunks[:top_k]
