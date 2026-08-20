from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from src.utils.logger import get_logger
from src.api.schemas import AnalyzeTicketRequest, SearchKnowledgeRequest, SearchKnowledgeResponse
from src.models.schemas import TicketAnalysis
from src.models.llm_agent import TicketAnalyzer
from src.rag.retrieval import DocumentRetriever

logger = get_logger(__name__)

from contextlib import asynccontextmanager

# Initialize global components (lazily or at startup)
_analyzer: Optional[TicketAnalyzer] = None
_retriever: Optional[DocumentRetriever] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _analyzer, _retriever
    logger.info("Initializing application components...")
    try:
        # These will read GOOGLE_API_KEY from environment
        _analyzer = TicketAnalyzer()
        _retriever = DocumentRetriever()
        logger.info("Components initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize components during startup: {e}")
        # Note: In a real app we might raise here or let endpoints handle missing components
    yield
    # Cleanup code could go here
    logger.info("Shutting down application...")

app = FastAPI(
    title="Support Ops Copilot API",
    description="API for customer support ticket analysis and knowledge retrieval.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    """Returns the health status of the API."""
    return {"status": "ok"}

@app.post("/analyze-ticket", response_model=TicketAnalysis, tags=["Analysis"])
def analyze_ticket(request: AnalyzeTicketRequest):
    """
    Analyzes a customer support ticket to extract priority, sentiment, and suggested actions.
    """
    if not _analyzer:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ticket analyzer component is not initialized."
        )
        
    try:
        result = _analyzer.analyze_ticket(subject=request.subject, description=request.description)
        return result
    except Exception as e:
        logger.error(f"Error during ticket analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze ticket."
        )

@app.post("/search-knowledge", response_model=SearchKnowledgeResponse, tags=["RAG"])
def search_knowledge(request: SearchKnowledgeRequest):
    """
    Searches the RAG knowledge base for relevant documents based on a query.
    """
    if not _retriever:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document retriever component is not initialized."
        )
        
    try:
        documents = _retriever.retrieve_similar(query=request.query, k=request.k)
        # Extract just the page content for the API response
        doc_contents = [doc.page_content for doc in documents]
        return SearchKnowledgeResponse(documents=doc_contents)
    except Exception as e:
        logger.error(f"Error during knowledge retrieval: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve knowledge."
        )
