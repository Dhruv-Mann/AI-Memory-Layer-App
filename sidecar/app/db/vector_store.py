import os  # to handle local file paths.
import lancedb  # database.
import pyarrow as pa # LanceDB relies on Pyarrow to define strict, columnar
                     # table schemas.
from typing import List
from app.ml.embeddings import generate_embedding # Imports a custom utility function that converts text
                                                 # to numerical vectors using an AI embedding model

# We store the vector DB inside the local app data or workspace to remain 100% local
DB_PATH = os.path.join(os.path.dirname(__file__), "../../../local_data/lancedb")

# Define the schema for LanceDB
schema = pa.schema([
    pa.field("vector", pa.list_(pa.float32(), 768)), # 768 dimensions for nomic-embed-text
    pa.field("text", pa.string()), # creates a column(text) to hold the raw text string associated with the vector
    pa.field("source", pa.string()) # creates a metadata column(source) to track where the document came from(eg: url,filename, etc)
])

# helper function to establish a connection with the database
def get_table():
    db = lancedb.connect(DB_PATH)
    if "memory_chunks" not in db.table_names():
        return db.create_table("memory_chunks", schema=schema) # create a new table if one does not exist.
    return db.open_table("memory_chunks")


# handles embedding new text and saving it directly to the database
def insert_document(text: str, source: str = "manual"):
    table = get_table()
    vector = generate_embedding(text)  # generates the 768-dimensional vector
    
    # Store the single text chunk with its vector and metadata(appends a new row in the database table)
    table.add([{
        "vector": vector,
        "text": text,
        "source": source
    }])
    return True  # returns true if the insertion was successful

# takes the user's query and searches the database for the most contextually relevant chunks
def search_documents(query: str, top_k: int = 3) -> List[dict]:
    table = get_table()  # opens the database table
    query_vector = generate_embedding(query)  # converts the user query into a 768-dimensional vector
    
    # Perform vector similarity search in the database
    results = table.search(query_vector).limit(top_k).to_list()
    return results
