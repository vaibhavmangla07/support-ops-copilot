import re
import string

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}")
CARD_PATTERN = re.compile(r"(?:\d[ -]*?){13,16}")

UNSUPPORTED_CLAIMS = [
    "i have reset your password",
    "refund issued",
    "your account has been unlocked",
    "i unlocked your account",
    "your ticket has been escalated",
    "i escalated your ticket",
    "i have issued the refund"
]

PROMPT_LEAKS = [
    "system prompt",
    "developer message",
    "internal instructions",
    "hidden prompt",
    "historical resolved tickets"
]

UNSAFE_INSTRUCTIONS = [
    "drop table",
    "delete from",
    "chmod -r 777",
    "rm -rf",
    "share your password",
    "what is your password"
]

STOPWORDS = {
    "the", "a", "an", "is", "and", "or", "to", "in", "of", "for",
    "with", "on", "it", "this", "that", "i", "you", "we", "your",
    "my", "please", "can", "will", "be", "are", "am", "have", "has",
    "do", "does", "not", "if", "let", "me", "know", "help", "thank",
    "thanks", "hello", "hi", "regards", "best"
}

def check_empty_invalid(response):
    text = response.strip().lower()
    return not text or text in {"error", "internal server error", "null", "none"} or len(text) < 10

def check_prompt_leak(response):
    text = response.lower()
    return any(item in text for item in PROMPT_LEAKS)

def check_unsafe_instruction(response):
    text = response.lower()
    return any(item in text for item in UNSAFE_INSTRUCTIONS)

def check_unsupported_action(response):
    text = response.lower()
    return any(item in text for item in UNSUPPORTED_CLAIMS)

def detect_and_redact_pii(response):
    text = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", response)
    text = CARD_PATTERN.sub("[REDACTED_CARD]", text)

    def redact_phone(match):
        value = match.group(0)
        digits = re.sub(r"\D", "", value)
        return "[REDACTED_PHONE]" if 10 <= len(digits) <= 15 else value

    text = PHONE_PATTERN.sub(redact_phone, text)
    return text != response, text

def check_grounding(response, ticket_text, retrieved_tickets):
    def get_words(text):
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()
        return set(text.split()) - STOPWORDS

    context_words = get_words(ticket_text)

    for ticket in retrieved_tickets:
        context_words.update(get_words(ticket["text"]))
        context_words.update(get_words(ticket["answer"]))

    response_words = get_words(response)

    if not response_words:
        return "WEAKLY_SUPPORTED"

    overlap = len(response_words & context_words) / len(response_words)
    return "SUPPORTED" if overlap >= 0.15 else "WEAKLY_SUPPORTED"

def apply_guardrails(response, ticket_text, retrieved_tickets):
    flags = []
    action = "ALLOW"
    final_response = response

    if check_empty_invalid(response):
        return {"passed": False, "action": "REVIEW", "flags": ["EMPTY_OR_INVALID"], "response": response}

    if check_prompt_leak(response):
        return {"passed": False, "action": "BLOCK", "flags": ["PROMPT_LEAK"], "response": response}

    if check_unsafe_instruction(response):
        return {"passed": False, "action": "BLOCK", "flags": ["UNSAFE_INSTRUCTION"], "response": response}

    if check_unsupported_action(response):
        flags.append("UNSUPPORTED_ACTION")
        action = "REVIEW"

    has_pii, final_response = detect_and_redact_pii(final_response)

    if has_pii:
        flags.append("PII_DETECTED")
        if action == "ALLOW":
            action = "REDACT"

    if check_grounding(final_response, ticket_text, retrieved_tickets) == "WEAKLY_SUPPORTED":
        flags.append("WEAK_GROUNDING")
        if action in {"ALLOW", "REDACT"}:
            action = "REVIEW"

    return {
        "passed": action in {"ALLOW", "REDACT"},
        "action": action,
        "flags": flags,
        "response": final_response
    }