# Support Ops Copilot

An AI-assisted support ticket triage and response-drafting system that combines machine learning, multilingual RAG, Gemini, and deterministic guardrails.

## 1. Problem

Support teams spend significant time manually categorizing, prioritizing, and searching historical tickets for solutions. This can increase response time and repetitive work.

Direct use of LLMs can also produce unsupported troubleshooting steps or unsafe instructions.

## 2. Solution

Support Ops Copilot automates ticket triage using machine learning and retrieves similar historical tickets using multilingual embeddings and FAISS.

The retrieved resolutions are provided to Gemini as context for response drafting. A deterministic guardrail layer then checks the generated response for PII, prompt leakage, unsafe instructions, unsupported actions, and weak grounding.

## 3. Architecture

```text
User Ticket
    ↓
Streamlit UI
    ↓
FastAPI API
    ↓
Category + Priority Classification
    ↓
FAISS RAG Retrieval
    ↓
Top-3 Historical Resolutions
    ↓
Gemini Response Generation
    ↓
Deterministic Guardrails
    ↓
Final Response
```

## 4. Features

- **Categorization & Prioritization**: Instant offline classification into standard IT categories and urgency levels.
- **RAG Knowledge Base**: Lightning-fast offline semantic retrieval of historical resolutions using FAISS.
- **Multilingual**: Natively supports English and German without intermediate translation APIs.
- **Deterministic Guardrails**: Protects against PII leakage, prompt injection, ungrounded generation, and unsafe server commands.
- **Decoupled API/UI**: A modular `FastAPI` backend paired with a lightweight `Streamlit` frontend.

## 5. Technology Stack

- **Python**: Core Language
- **Scikit-Learn & Joblib**: ML Classification pipeline
- **Sentence-Transformers**: Multilingual embeddings (`paraphrase-multilingual-MiniLM-L12-v2`)
- **FAISS**: Vector Database (`IndexFlatIP`)
- **FastAPI**: Backend API
- **Streamlit**: Frontend Dashboard
- **Google GenAI**: Response drafting (Gemini 1.5 Flash)

## 6. Dataset

Trained on synthetic multi-lingual IT support datasets mapping tickets to historical resolutions. The `answer` feature was strictly dropped from ML classification features to prevent data leakage.

## 7. Project Structure

```
├── datasets/        # Raw and processed datasets
├── models/          # Trained joblib models and FAISS index
├── notebooks/       # EDA and training notebooks
├── src/             # Source code (API, RAG, Frontend, Guardrails, Evals)
├── .env.example     # Environment variable template
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 8. Installation

1. Clone the repository.
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and insert your `GEMINI_API_KEY`.

## 9. Running Instructions

### 1. Start the API Backend

Open a terminal and run the FastAPI server:

```bash
source .venv/bin/activate
export PYTHONPATH=.
uvicorn src.api.main:app --port 8001
```

### 2. Start the Streamlit Frontend

Open a new terminal and run the UI:

```bash
source .venv/bin/activate
export PYTHONPATH=.
streamlit run src/frontend/app.py
```

Navigate to `http://localhost:8501`.

## 10. Model Results

- **Category Classification**: Accuracy = 84.24% | Macro F1 = 0.8510
- **Priority Classification**: Accuracy = 56.14% | Macro F1 = 0.5458

## 11. RAG Results

- **Recall@1**: 95.40%
- **Recall@3**: 99.20%
- **Recall@5**: 99.80%
- **Recall@10**: 100.00%

## 12. Limitations

- **Priority Classification**: Dataset noise (arbitrary historical labels) fundamentally caps performance.
- **LLM Evaluation**: Real-time linguistic metrics cannot be auto-generated without live API keys.
- **Grounding Limitations**: Guardrail relies on strict vocabulary-overlap and can be bypassed by dense obfuscation or synonym rewrites.
- **Single LLM Provider**: Currently hardcoded to Google Gemini.

## 13. Future Improvements

- Refine Priority labels through active learning or human-in-the-loop feedback.
- Introduce advanced PII reduction pipelines (e.g. Presidio).
- Decouple LLM provider via standard LangChain integrations where enterprise complexity is justified.
- Implement proper Authentication schemas (JWT/OAuth2) for the FastAPI backend.
