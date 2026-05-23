from sentence_transformers import SentenceTransformer  # allows us to run open source text embeddings locally
import time

# Cache the model globally so we don't reload it for every single chunk
print("Initializing Embedding Engine...")
EMBEDDING_MODEL = SentenceTransformer("nomic-ai/nomic-embed-text-v2-moe", trust_remote_code=True)

def generate_embedding(text: str):  # the main utility function which accepts string parameter.
    # Generate the vector
    start_time = time.time()  # starting the timer
    vector = EMBEDDING_MODEL.encode(text)  # starting the embedding
    end_time = time.time()  # stopping the timer
    
    print(f"\nSuccess! Generated a vector with {len(vector)} dimensions.") # tells the vector dimensions(768)
    print(f"Time taken: {round(end_time - start_time, 3)} seconds.")  # tells the total time taken
    
    # Convert numpy array to list so it can be stored in LanceDB easily
    vector_list = vector.tolist() 
    print(f"First 5 numbers of the vector: {vector_list[:5]}")
    
    return vector_list

if __name__ == "__main__":
    # Test our function directly
    sample_text = "Dynamic Programming is a method for solving complex problems by breaking them down into simpler subproblems."
    generate_embedding(sample_text)
