# Environment Setup & Verification

## 1. Python Version
**Version:** Python 3.11.9
**Executable:** `.venv/bin/python`

## 2. Virtual Environment
**Name:** `.venv`
**Location:** Project root (`support-ops-copilot/.venv`)

## 3. Dependency Management Approach
Standard Python `pip` mapped to a single isolated `requirements.txt` file. We avoided heavy wrappers like Conda or Poetry to adhere to the principle of "simplicity beats complexity."

## 4. Installation Method
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Important Packages Verified
All required libraries successfully import without errors:
- Data & Visualization: `numpy`, `pandas`, `matplotlib`, `seaborn`
- Traditional ML: `scikit-learn`, `xgboost`, `optuna`
- NLP & Deep Learning: `nltk`, `torch`
- Generative AI: `langchain`, `langgraph`
- Server & Database: `fastapi`, `uvicorn`, `sqlite3`
- Frontend: `streamlit`

## 6. Environment Variable Setup
- **`.env.example`**: Contains placeholders for `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and DB credentials.
- **Security Check**: `.env` is fully excluded via `.gitignore` to prevent secret leakage. No actual keys have been hardcoded.

## 7. Verification Steps
Executed via `src/utils/health_check.py`.
- **PyTorch Test**: Successfully created tensors and performed addition (`torch.tensor([1., 2., 3.]) + tensor([4., 5., 6.]) = tensor([5., 7., 9.])`).
- **Dataset Test**: Verified that `datasets/raw/aa_dataset-tickets-multi-lang-5-2-50-version.csv` and `customer_support_tickets.csv` exist and are readable on disk.

## 8. Common Setup Issues Encountered
- **Missing Requirements**: During initial verification, `matplotlib` and `seaborn` threw `ModuleNotFoundError` because they were absent from the original `requirements.txt`.
- **Resolution**: Updated `requirements.txt` under the Data Science section and re-ran `pip install` successfully.

## 9. Final Environment Status
**Status:** FULLY VERIFIED. Environment is stable and locked. Ready for Phase 3.
