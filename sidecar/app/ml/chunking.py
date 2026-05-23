from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(text: str, chunk_size: int = 1500) -> list[str]:
    """
    Slices a large document into optimal semantic chunks before embedding.
    """
    # 15% loop back for much more effective chunking
    overlap_size = int(chunk_size * 0.15) 
    
    # Configure the Recursive Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        # The recursive priority list: Paragraphs -> Lines -> Words -> Chars
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Generate and return the list of text chunks
    chunks = text_splitter.split_text(text)
    
    return chunks
