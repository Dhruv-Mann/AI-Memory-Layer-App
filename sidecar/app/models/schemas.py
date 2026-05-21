from pydantic import BaseModel
from typing import List, Optional

class DocumentIngest(BaseModel):
    text: str
    metadata: dict = {}

class ChatQuery(BaseModel):
    query: str
    top_k: int = 3

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
