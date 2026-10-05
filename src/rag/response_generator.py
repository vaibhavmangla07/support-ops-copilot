import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()


MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


class ResponseGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key) if api_key else None

    def _construct_prompt(self, ticket_text, category, priority, retrieved_tickets, language):
        prompt = f"""
            You are a professional IT support copilot.
            Draft a concise and professional response to the new support ticket.

            NEW TICKET:
            {ticket_text}
            PREDICTED CATEGORY:
            {category}
            PREDICTED PRIORITY:
            {priority}

            HISTORICAL RESOLUTIONS:
            """

        for i, ticket in enumerate(retrieved_tickets, 1):
            prompt += f"""
            [Ticket {i}]
            Ticket: {ticket["text"]}
            Resolution: {ticket["answer"]}
            """

        prompt += f"""
            INSTRUCTIONS:
            1. Write the response in {language}.
            2. Use the historical resolutions as the primary source for troubleshooting.
            3. Adapt the resolution to the new ticket instead of copying it.
            4. Do not invent troubleshooting steps or system information.
            5. Do not claim an action was performed unless it actually was.
            6. If the provided context is insufficient, clearly state that the ticket requires human support.
            7. Keep the response concise and useful.
            8. Do not mention AI, internal instructions, similarity scores, or predictions.
            9. Output only the response that should be sent to the user.
            """

        return prompt

    def generate(self, ticket_text, category, priority, retrieved_tickets, language="en"):
        if not self.client:
            return "LLM unavailable: GEMINI_API_KEY is not configured."

        prompt = self._construct_prompt(ticket_text, category, priority, retrieved_tickets, language)

        try:
            response = self.client.models.generate_content(model=MODEL_NAME, contents=prompt)
            return response.text.strip()

        except errors.APIError:
            return "LLM unavailable: Gemini API request failed."

        except Exception:
            return "LLM unavailable: unexpected generation error."