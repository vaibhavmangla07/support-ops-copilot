import os
import json
import faiss
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_STORE_DIR = "models/vector_store"


class TicketRetriever:
    def __init__(self):
        index_path = os.path.join(VECTOR_STORE_DIR, "support_tickets.index")
        metadata_path = os.path.join(VECTOR_STORE_DIR, "metadata.json")

        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def retrieve(self, query, top_k=5, exclude_id=None):
        query_embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)

        search_k = top_k + 1 if exclude_id is not None else top_k
        scores, indices = self.index.search(query_embedding, search_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            metadata = self.metadata[index]

            if exclude_id is not None and metadata.get("document_id") == exclude_id:
                continue

            results.append({
                "text": metadata["text"],
                "answer": metadata["answer"],
                "category": metadata["type"],
                "priority": metadata.get("priority", "unknown"),
                "language": metadata["language"],
                "score": float(score)
            })

            if len(results) >= top_k:
                break

        return results


if __name__ == "__main__":
    retriever = TicketRetriever()
    print("Retriever loaded successfully. Index size:", retriever.index.ntotal)