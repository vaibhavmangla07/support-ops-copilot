import os
from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DocumentIngestor:
    """
    Handles ingestion of documents into a local ChromaDB vector store.
    """
    def __init__(self, persist_directory: str = "./data/chroma_db", api_key: str = None):
        self.persist_directory = persist_directory
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. Embeddings will fail without it.")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", 
            google_api_key=self.api_key
        )
        
    def ingest_documents(self, documents: List[Document]) -> Chroma:
        """
        Embeds and stores a list of LangChain Document objects into Chroma.
        """
        logger.info(f"Ingesting {len(documents)} documents into Chroma vector store at {self.persist_directory}")
        try:
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            # In latest langchain-chroma persist is automatic or handled on exit,
            # but calling persist if it exists is safe practice.
            if hasattr(vectorstore, 'persist'):
                vectorstore.persist()
            logger.info("Ingestion complete.")
            return vectorstore
        except Exception as e:
            logger.error(f"Error during document ingestion: {e}")
            raise
