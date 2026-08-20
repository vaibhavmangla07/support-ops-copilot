import os
from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DocumentRetriever:
    """
    Handles retrieving documents from the local ChromaDB vector store.
    """
    def __init__(self, persist_directory: str = "./data/chroma_db", api_key: str = None):
        self.persist_directory = persist_directory
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", 
            google_api_key=self.api_key
        )
        
        self.vectorstore = self._load_vectorstore()

    def _load_vectorstore(self) -> Chroma:
        logger.info(f"Loading Chroma vector store from {self.persist_directory}")
        if not os.path.exists(self.persist_directory):
            logger.warning(f"Directory {self.persist_directory} does not exist. The store may be empty.")
            
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def retrieve_similar(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieves the top k most similar documents to the query.
        """
        logger.info(f"Retrieving top {k} documents for query: '{query}'")
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Retrieved {len(results)} documents.")
            return results
        except Exception as e:
            logger.error(f"Error during document retrieval: {e}")
            raise
