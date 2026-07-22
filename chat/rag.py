from sentence_transformers import SentenceTransformer
import numpy as np

from .rag_documents import DOCUMENTS

# Loaded ONCE, at import time (i.e. once per Django process, not per request).
# Loading this model takes real time (~seconds) — doing it inside the view
# would mean every single request pays that cost. Same "lazy singleton"
# pattern as the anthropic client, just eager here since embedding the
# documents also needs to happen once.
_embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed every document once, upfront, at process startup — reused for
# every request afterward instead of recomputed each time.
_doc_embeddings = _embed_model.encode(DOCUMENTS)


def _cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_relevant_chunks(question: str, top_k: int = 2):
    """Returns the top_k most relevant documents for a question, each
    paired with its similarity score."""
    question_embedding = _embed_model.encode(question)
    scores = [_cosine_similarity(question_embedding, doc_emb) for doc_emb in _doc_embeddings]
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(DOCUMENTS[i], float(scores[i])) for i in top_indices]