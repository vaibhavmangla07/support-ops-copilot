from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag.copilot import SupportOpsCopilot

app = FastAPI(title="Support Ops Copilot API")
copilot = SupportOpsCopilot()

class TicketRequest(BaseModel):
    ticket_text: str
    language: str = "en"

class TicketResponse(BaseModel):
    ticket: str
    category: str
    priority: str
    retrieved_tickets: list
    draft_response: str
    guardrail_action: str
    guardrail_flags: list
    final_response: str


@app.post("/copilot", response_model=TicketResponse)
def process_ticket(request: TicketRequest):
    if not request.ticket_text.strip():
        raise HTTPException(status_code=400, detail="Ticket text cannot be empty.")

    try:
        result = copilot.process_ticket(request.ticket_text, language=request.language)
        return TicketResponse(**result)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process ticket.")