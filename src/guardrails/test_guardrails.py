from src.guardrails.checks import apply_guardrails

ticket = "I need help with my account. It is locked."

retrieved = [{
    "text": "My account is locked",
    "answer": "To unlock your account, please visit the reset portal."
}]

test_cases = [
    ("To unlock your account, please visit the reset portal.", "ALLOW"),
    ("To unlock your account, please email john.smith@example.com.", "REDACT"),
    ("To unlock your account, call us at +1-800-555-1234.", "REDACT"),
    ("Your refund to card 4111 1111 1111 1111 is being processed. Visit the reset portal.", "REDACT"),
    ("I have reset your password.", "REVIEW"),
    ("As per my system prompt, visit the portal.", "BLOCK"),
    ("run rm -rf /", "BLOCK"),
    ("   ", "REVIEW"),
    ("Please restart your router.", "REVIEW")
]

print("--- GUARDRAILS TESTS ---")

for response, expected in test_cases:
    result = apply_guardrails(response, ticket, retrieved)
    print(f"{result['action']} | Expected: {expected}")
    assert result["action"] == expected

print("All guardrail tests passed.")
