from pydantic import BaseModel  # type enforcement, type coercion, error catching.
from typing import List, Optional  # standard python typing utilities.

# This class defines what a piece of text looks like when it is being uploaded
# or stored in a database.
class DocumentIngest(BaseModel): # New pydantic model called DocumentIngest.
    text: str  # defines a required field called text which must be a string.
    metadata: dict = {}  # defines an optional field called metadata which must be a dictionary
                         # (used for extra info like url, date, author etc) -> if not provided then it
                         # automatically defaults to an empty dict.


# This class defines the incoming question from the user
class ChatQuery(BaseModel):
    query: str  # query must be string
    top_k: int = 3  # defines the number of source documents the system should retrieve to answer the query.
    tags: Optional[List[str]] = None
    file_type: Optional[str] = None
    model: Optional[str] = None

# This class defines the structural output which the AI will send to the user.
class ChatResponse(BaseModel):
    answer: str  # answer must be string.
    sources: List[str] #  A list of strings which contains the names, links, or text snippets to formulate
                       # the final answer.

class GradeRequest(BaseModel):
    card_id: str
    grade: int # 1=Again, 2=Hard, 3=Good, 4=Easy
