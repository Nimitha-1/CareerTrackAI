from sentence_transformers import SentenceTransformer

def get_embedding_model():
    """
    Load the Sentence-BERT model for embeddings (used in RAG).
    """
    return SentenceTransformer("all-MiniLM-L6-v2")
