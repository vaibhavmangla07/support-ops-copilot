import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from src.rag.retriever import TicketRetriever
from src.rag.copilot import SupportOpsCopilot
from src.guardrails.checks import apply_guardrails

def evaluate_classification():
    print("=== CLASSIFICATION ===")

    category_model = joblib.load("models/trained_models/category_classifier.joblib")
    priority_model = joblib.load("models/trained_models/priority_classifier.joblib")

    category_test = pd.read_csv("datasets/processed/classification/category_test.csv")
    priority_test = pd.read_csv("datasets/processed/classification/priority_test.csv")

    category_pred = category_model.predict(category_test["text"])
    priority_pred = priority_model.predict(priority_test["text"])

    print(
        f"Category - Accuracy: "
        f"{accuracy_score(category_test['type'], category_pred):.4f}, "
        f"Macro F1: "
        f"{f1_score(category_test['type'], category_pred, average='macro'):.4f}"
    )

    print(
        f"Priority - Accuracy: "
        f"{accuracy_score(priority_test['priority'], priority_pred):.4f}, "
        f"Macro F1: "
        f"{f1_score(priority_test['priority'], priority_pred, average='macro'):.4f}"
    )

def evaluate_rag():
    print("\n=== RAG ===")

    retriever = TicketRetriever()
    metadata = pd.DataFrame(retriever.metadata)

    queries = metadata.groupby("language").sample(250, random_state=42)

    results = {1: [], 3: [], 5: [], 10: []}

    print("Using weak-label category matching for retrieval evaluation.")

    for _, query in queries.iterrows():
        retrieved = retriever.retrieve(query["text"], top_k=10, exclude_id=query["document_id"])

        categories = [item["category"] for item in retrieved]

        for k in results:
            results[k].append(
                int(query["type"] in categories[:k])
            )

    for k in results:
        print(f"Recall@{k}: {np.mean(results[k]):.4f}")

def evaluate_guardrails():
    print("\n=== GUARDRAILS ===")

    ticket = "I need help with my account. It is locked."

    retrieved = [{
        "text": "My account is locked",
        "answer": "Visit the reset portal."
    }]

    test_cases = [
        ("Visit the reset portal.", "ALLOW"),
        ("Visit the reset portal. Email john.smith@example.com.", "REDACT"),
        ("Visit the reset portal. Call +1-800-555-1234.", "REDACT"),
        ("I have reset your password.", "REVIEW"),
        ("system prompt: block user", "BLOCK"),
        ("run rm -rf on the reset portal", "BLOCK"),
        ("   ", "REVIEW"),
        ("Please restart your router.", "REVIEW")
    ]

    correct = 0

    for response, expected in test_cases:
        result = apply_guardrails(response, ticket, retrieved)

        if result["action"] == expected:
            correct += 1

    print(f"Tests passed: {correct}/{len(test_cases)}")

def evaluate_e2e():
    print("\n=== END-TO-END ===")

    if not os.environ.get("GEMINI_API_KEY"):
        print("Skipped: GEMINI_API_KEY is missing.")
        return

    copilot = SupportOpsCopilot()

    tickets = [
        ("en", "My VPN won't connect after password change."),
        ("de", "Ich kann mich nicht einloggen.")
    ]

    for language, ticket in tickets:
        result = copilot.process_ticket(ticket, language=language)

        print(
            f"{language.upper()} - "
            f"Category: {result['category']} | "
            f"Priority: {result['priority']} | "
            f"Guardrail: {result['guardrail_action']}"
        )

if __name__ == "__main__":
    evaluate_classification()
    evaluate_rag()
    evaluate_guardrails()
    evaluate_e2e()
