from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity(text1: str, text2: str) -> float:
    emb = model.encode([text1, text2])
    score = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return round(score * 100, 2)
