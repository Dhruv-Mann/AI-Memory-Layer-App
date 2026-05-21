from sentence_transformers import SentenceTransformer
import time

def generate_embedding(text: str):
    print(f"Loading embedding model... (This might take a minute the first time to download)")
    
    # We are using 'nomic-embed-text-v1.5' (or v2) configured for local CPU inference.
    # trust_remote_code=True is required for Nomic models via sentence-transformers.
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
    
    print(f"\nModel loaded! Embedding text: '{text}'")
    
    # Generate the vector
    start_time = time.time()
    vector = model.encode(text)
    end_time = time.time()
    
    print(f"\nSuccess! Generated a vector with {len(vector)} dimensions.")
    print(f"Time taken: {round(end_time - start_time, 3)} seconds.")
    
    # Convert numpy array to list so it can be stored in LanceDB easily
    vector_list = vector.tolist()
    print(f"First 5 numbers of the vector: {vector_list[:5]}")
    
    return vector_list

if __name__ == "__main__":
    # Test our function directly
    sample_text = "Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems."
    generate_embedding(sample_text)
