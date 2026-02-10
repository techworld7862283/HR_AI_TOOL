from sklearn.metrics.pairwise import cosine_similarity

_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def similarity(text1: str, text2: str) -> float:
    model = get_model()
    emb = model.encode([text1, text2])
    score = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return round(score * 100, 2)

