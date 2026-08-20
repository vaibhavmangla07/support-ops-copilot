import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from src.models.schemas import TicketAnalysis
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TicketAnalyzer:
    """
    LLM-powered agent to analyze customer support tickets.
    Uses Google Gemini and Langchain for structured output extraction.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash", api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. TicketAnalyzer may fail to initialize.")
            
        self.model_name = model_name
        self.parser = PydanticOutputParser(pydantic_object=TicketAnalysis)
        self.llm = self._initialize_llm()
        self.chain = self._build_chain()

    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        logger.info(f"Initializing ChatGoogleGenerativeAI with model: {self.model_name}")
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=0.0
        )

    def _build_chain(self):
        system_prompt = (
            "You are an expert customer support operations assistant. "
            "Your task is to analyze customer support tickets and extract structured information.\n\n"
            "{format_instructions}"
        )
        human_prompt = (
            "Please analyze the following ticket.\n"
            "Subject: {subject}\n"
            "Description: {description}\n"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt),
        ])
        
        return prompt | self.llm | self.parser

    def analyze_ticket(self, subject: str, description: str) -> TicketAnalysis:
        """
        Analyzes a single ticket and returns structured insights.
        """
        logger.info(f"Analyzing ticket: {subject}")
        try:
            result = self.chain.invoke({
                "subject": subject,
                "description": description,
                "format_instructions": self.parser.get_format_instructions()
            })
            logger.info("Successfully analyzed ticket.")
            return result
        except Exception as e:
            logger.error(f"Failed to analyze ticket. Error: {e}")
            raise
