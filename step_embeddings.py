from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")  # downloads once, caches locally after

sentences = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "Django is a Python web framework.",
]

embeddings = model.encode(sentences)

print("Shape:", embeddings.shape)  # (3, 384) — 3 sentences, 384 numbers each

# Cosine similarity: measures the angle between two vectors, not their length.
# REFER The below site i used for understanding cosine similarity: 
# https://medium.com/@charan4u/unlocking-the-power-of-cosine-similarity-the-heart-of-text-understanding-eed427df745a
# 1.0 = identical meaning direction, 0 = unrelated, -1 = opposite.
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\ncat/mat vs feline/rug:", cosine_similarity(embeddings[0], embeddings[1]))
print("cat/mat vs Django:", cosine_similarity(embeddings[0], embeddings[2]))

"""
My Output:
Shape: (3, 384)

cat/mat vs feline/rug: 0.5559763
cat/mat vs Django: 0.013242047
"""