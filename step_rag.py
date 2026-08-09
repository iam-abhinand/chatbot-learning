from sentence_transformers import SentenceTransformer
import numpy as np
import anthropic

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = anthropic.Anthropic()

# Our tiny "knowledge base" — normally this would come from real documents,
# split into chunks. Kept as plain strings here to isolate the RAG concept
# from document-parsing concerns.
documents = [
    "The claude-chatbot project uses Django REST Framework for the backend API.",
    "The frontend is built with React and Vite, running on port 5173 by default.",
    "Docker Compose is used to run the backend and frontend together locally.",
    "The project uses the sliding window strategy to manage context window size.",
    "Paris is the capital of France and home to the Eiffel Tower.",
]

# Embed every document once, upfront.
doc_embeddings = embed_model.encode(documents)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_relevant_chunks(question: str, top_k: int = 2):
    question_embedding = embed_model.encode(question)
    scores = [cosine_similarity(question_embedding, doc_emb) for doc_emb in doc_embeddings]
    # Get indices of the top_k highest-scoring documents
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(documents[i], scores[i]) for i in top_indices]


question = "What frontend framework does this project use?"
retrieved = retrieve_relevant_chunks(question)

print("--- Retrieved chunks ---")
for doc, score in retrieved:
    print(f"[{score:.3f}] {doc}")

# Now inject ONLY the retrieved chunks into the prompt — not all 5 documents.
context = "\n".join(doc for doc, _ in retrieved)

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    system=f"Answer the user's question using only this context:\n\n{context}",
    messages=[{"role": "user", "content": question}],
)

print("\n--- Claude's answer ---")
print(response.content[0].text)


"""
The OUTPUT : 
--- Retrieved chunks ---
[0.496] The frontend is built with React and Vite, running on port 5173 by default.
[0.491] Docker Compose is used to run the backend and frontend together locally.

--- Claude's answer ---
According to the provided context, this project uses **React** as the frontend framework, with **Vite** as the build tool. The frontend runs on port 5173 by default.
"""