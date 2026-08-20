from pydantic import BaseModel, Field
from typing import List

class AnalyzeTicketRequest(BaseModel):
    subject: str = Field(..., description="The subject line of the customer ticket.")
    description: str = Field(..., description="The full body text of the customer ticket.")

class SearchKnowledgeRequest(BaseModel):
    query: str = Field(..., description="The user's query to search the knowledge base for.")
    k: int = Field(default=3, ge=1, le=10, description="The number of documents to retrieve.")

class SearchKnowledgeResponse(BaseModel):
    documents: List[str] = Field(description="The top retrieved documents from the knowledge base.")
