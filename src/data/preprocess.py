import os
import pandas as pd
from sklearn.model_selection import train_test_split


RAW_FILE = "datasets/raw/aa_dataset-tickets-multi-lang-5-2-50-version.csv"
CLASSIFICATION_DIR = "datasets/processed/classification"
RAG_DIR = "datasets/processed/rag"


df = pd.read_csv(RAW_FILE, low_memory=False)

print("Raw dataset:", df.shape)

# Clean text
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")
df["answer"] = df["answer"].fillna("")

df["text"] = (df["subject"] + " " + df["body"]).str.replace(
    r"\s+", " ", regex=True
).str.strip()

df["answer"] = df["answer"].str.replace(
    r"\s+", " ", regex=True
).str.strip()

# Keep rows with classification labels
df = df.dropna(subset=["type", "priority"])

# -------------------------
# RAG Knowledge Base
# -------------------------

rag_df = df[(df["text"] != "") & (df["answer"] != "")].copy()
rag_df = rag_df[["text", "answer", "language", "type", "queue"]]
rag_df["document_id"] = range(1, len(rag_df) + 1)

os.makedirs(RAG_DIR, exist_ok=True)

rag_df.to_csv(f"{RAG_DIR}/knowledge_base.csv", index=False)
print("RAG knowledge base:", rag_df.shape)

# -------------------------
# Classification Dataset
# -------------------------

class_df = df[["text", "language", "type", "priority"]].copy()
class_df = class_df[class_df["text"] != ""]
class_df = class_df.drop_duplicates(subset=["text", "type", "priority"])

os.makedirs(CLASSIFICATION_DIR, exist_ok=True)

# Category split
category_train, category_temp = train_test_split(class_df, test_size=0.30, stratify=class_df["type"], random_state=42)

category_val, category_test = train_test_split(category_temp, test_size=0.50, stratify=category_temp["type"], random_state=42)

category_train[["text", "language", "type"]].to_csv(f"{CLASSIFICATION_DIR}/category_train.csv", index=False)
category_val[["text", "language", "type"]].to_csv(f"{CLASSIFICATION_DIR}/category_validation.csv", index=False)
category_test[["text", "language", "type"]].to_csv(f"{CLASSIFICATION_DIR}/category_test.csv", index=False)

# Priority split
priority_train, priority_temp = train_test_split(class_df, test_size=0.30, stratify=class_df["priority"], random_state=42)
priority_val, priority_test = train_test_split(priority_temp, test_size=0.50, stratify=priority_temp["priority"], random_state=42)

priority_train[["text", "language", "priority"]].to_csv(f"{CLASSIFICATION_DIR}/priority_train.csv", index=False)
priority_val[["text", "language", "priority"]].to_csv(f"{CLASSIFICATION_DIR}/priority_validation.csv", index=False)
priority_test[["text", "language", "priority"]].to_csv(f"{CLASSIFICATION_DIR}/priority_test.csv", index=False)

print("Classification datasets created.")
print("Preprocessing completed.")