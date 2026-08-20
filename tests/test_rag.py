import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from src.rag.ingestion import DocumentIngestor
from src.rag.retrieval import DocumentRetriever

@pytest.fixture
def sample_documents():
    return [
        Document(page_content="How to reset password", metadata={"source": "faq"}),
        Document(page_content="Billing cycle information", metadata={"source": "billing"}),
    ]

@patch("src.rag.ingestion.Chroma")
@patch("src.rag.ingestion.GoogleGenerativeAIEmbeddings")
def test_document_ingestor(mock_embeddings, mock_chroma, sample_documents):
    ingestor = DocumentIngestor(api_key="fake_key", persist_directory="./dummy_dir")
    
    mock_vectorstore = MagicMock()
    mock_chroma.from_documents.return_value = mock_vectorstore
    
    vectorstore = ingestor.ingest_documents(sample_documents)
    
    mock_chroma.from_documents.assert_called_once()
    assert vectorstore == mock_vectorstore
    if hasattr(mock_vectorstore, 'persist'):
        mock_vectorstore.persist.assert_called_once()

@patch("src.rag.retrieval.Chroma")
@patch("src.rag.retrieval.GoogleGenerativeAIEmbeddings")
def test_document_retriever(mock_embeddings, mock_chroma, sample_documents):
    mock_vectorstore = MagicMock()
    # Return one document for similarity search
    mock_vectorstore.similarity_search.return_value = [sample_documents[0]]
    mock_chroma.return_value = mock_vectorstore
    
    retriever = DocumentRetriever(api_key="fake_key", persist_directory="./dummy_dir")
    results = retriever.retrieve_similar("password reset", k=1)
    
    mock_vectorstore.similarity_search.assert_called_once_with("password reset", k=1)
    assert len(results) == 1
    assert results[0].page_content == "How to reset password"
