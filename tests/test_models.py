import pytest
from unittest.mock import MagicMock, patch
from src.models.schemas import TicketAnalysis
from src.models.llm_agent import TicketAnalyzer

@pytest.fixture
def mock_ticket_analysis():
    return TicketAnalysis(
        priority="High",
        category="Technical Support",
        sentiment="Negative",
        tags=["login", "error"],
        suggested_action="Reset password and check logs."
    )

@patch("src.models.llm_agent.ChatGoogleGenerativeAI")
def test_ticket_analyzer_init(mock_llm):
    # Test initialization without API key
    analyzer = TicketAnalyzer(api_key="fake_key")
    assert analyzer.model_name == "gemini-1.5-flash"
    assert analyzer.api_key == "fake_key"
    mock_llm.assert_called_once()

@patch("src.models.llm_agent.TicketAnalyzer._build_chain")
@patch("src.models.llm_agent.ChatGoogleGenerativeAI")
def test_analyze_ticket(mock_llm, mock_build_chain, mock_ticket_analysis):
    # Setup mock chain
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = mock_ticket_analysis
    mock_build_chain.return_value = mock_chain
    
    analyzer = TicketAnalyzer(api_key="fake_key")
    
    result = analyzer.analyze_ticket("Cannot login", "I have been trying to login for 3 hours and keep getting a 500 error.")
    
    assert isinstance(result, TicketAnalysis)
    assert result.priority == "High"
    assert result.sentiment == "Negative"
    mock_chain.invoke.assert_called_once()
