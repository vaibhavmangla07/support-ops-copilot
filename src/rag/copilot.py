import joblib

from src.rag.retriever import TicketRetriever
from src.rag.response_generator import ResponseGenerator
from src.guardrails import apply_guardrails


class SupportOpsCopilot:
    def __init__(self):
        self.category_clf = joblib.load("models/trained_models/category_classifier.joblib")
        self.priority_clf = joblib.load("models/trained_models/priority_classifier.joblib")
        self.retriever = TicketRetriever()
        self.generator = ResponseGenerator()

    def process_ticket(self, ticket_text, language="en"):
        category = self.category_clf.predict([ticket_text])[0]
        priority = self.priority_clf.predict([ticket_text])[0]

        retrieved_tickets = self.retriever.retrieve(ticket_text, top_k=3)

        draft_response = self.generator.generate(ticket_text=ticket_text, category=category, priority=priority, retrieved_tickets=retrieved_tickets, language=language)

        guardrail_result = apply_guardrails(draft_response, ticket_text, retrieved_tickets)

        return {
            "ticket": ticket_text,
            "category": category,
            "priority": priority,
            "retrieved_tickets": retrieved_tickets,
            "draft_response": draft_response,
            "guardrail_action": guardrail_result["action"],
            "guardrail_flags": guardrail_result["flags"],
            "final_response": guardrail_result["response"]
        }