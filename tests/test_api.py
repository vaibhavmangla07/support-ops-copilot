import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.api.main import app
from src.models.schemas import TicketAnalysis
from langchain_core.documents import Document

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("src.api.main._analyzer")
def test_analyze_ticket(mock_analyzer):
    # Mock the return value of analyze_ticket
    mock_analyzer.analyze_ticket.return_value = TicketAnalysis(
        priority="High",
        category="Technical",
        sentiment="Negative",
        tags=["login"],
        suggested_action="Reset password."
    )
    
    response = client.post(
        "/analyze-ticket",
        json={"subject": "Login failed", "description": "I cannot login."}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "High"
    assert data["category"] == "Technical"

@patch("src.api.main._retriever")
def test_search_knowledge(mock_retriever):
    # Mock the return value of retrieve_similar
    mock_retriever.retrieve_similar.return_value = [
        Document(page_content="Here is how you reset a password.", metadata={})
    ]
    
    response = client.post(
        "/search-knowledge",
        json={"query": "password reset", "k": 1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 1
    assert data["documents"][0] == "Here is how you reset a password."

def test_analyze_ticket_missing_fields():
    response = client.post(
        "/analyze-ticket",
        json={"subject": "Login failed"} # missing description
    )
    # Should fail validation (422 Unprocessable Entity)
    assert response.status_code == 422
