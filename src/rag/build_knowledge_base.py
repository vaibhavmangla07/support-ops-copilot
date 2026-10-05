import os
import json
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer


DATA_PATH = "datasets/processed/rag/knowledge_base.csv"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_STORE_DIR = "models/vector_store"


def build_knowledge_base():
    print("Loading knowledge base...")
    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("Knowledge base is empty.")

    if df["text"].isna().any() or (df["text"] == "").any():
        raise ValueError("Knowledge base contains empty ticket text.")

    if df["answer"].isna().any() or (df["answer"] == "").any():
        raise ValueError("Knowledge base contains empty answers.")

    print(f"Loaded {len(df)} records.")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")
    embeddings = model.encode(df["text"].tolist(), show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)

    print("Building FAISS index...")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    index_path = os.path.join(VECTOR_STORE_DIR, "support_tickets.index")
    metadata_path = os.path.join(VECTOR_STORE_DIR, "metadata.json")

    faiss.write_index(index, index_path)

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False)

    print(f"FAISS index saved: {index_path}")
    print(f"Metadata saved: {metadata_path}")
    print("Knowledge base construction completed.")


if __name__ == "__main__":
    build_knowledge_base()