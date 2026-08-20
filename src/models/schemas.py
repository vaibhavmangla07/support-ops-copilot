from pydantic import BaseModel, Field
from typing import List

class TicketAnalysis(BaseModel):
    """Schema for structured output from ticket analysis."""
    
    priority: str = Field(
        description="The predicted priority of the ticket. Must be one of: 'Low', 'Medium', 'High', 'Critical'"
    )
    category: str = Field(
        description="The general category of the issue (e.g., 'Technical Support', 'Billing', 'General Inquiry', 'Feedback')"
    )
    sentiment: str = Field(
        description="The sentiment of the customer based on the ticket description. Must be one of: 'Positive', 'Neutral', 'Negative'"
    )
    tags: List[str] = Field(
        description="A list of 2-4 short tags describing the specific topics of the ticket.",
        max_length=4
    )
    suggested_action: str = Field(
        description="A brief, one-sentence suggestion on how the support agent should handle this ticket."
    )
