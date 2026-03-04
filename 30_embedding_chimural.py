# ============================================================
# Step 3 — Generate Embeddings from search_text
#
# What are embeddings?
# --------------------
# Embeddings convert text into a numeric vector (a list of floats).
# Similar text → similar vectors.
#
# Why do we need them?
# --------------------
# We’ll use embeddings to do semantic search:
# - Convert the mural descriptions into vectors
# - Convert a user query into a vector
# - Find the nearest mural vectors to the query vector
#
# Input column:
# - df_norm["search_text"]  (created during normalization)
# Output:
# - embeddings: numpy array with shape (num_rows, embedding_dim)
# ============================================================

%pip -q install sentence-transformers
import numpy as np
from sentence_transformers import SentenceTransformer

# A strong small model for semantic search demos (fast + decent quality)
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# Load embedding model
embed_model = SentenceTransformer(EMBED_MODEL_NAME)

texts = df_norm["search_text"].fillna("").tolist()

# Create embeddings
embeddings = embed_model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True,  # makes cosine similarity easy
)

print("Embeddings shape:", embeddings.shape)   # (rows, dim)
print("Embedding dim:", embeddings.shape[1])
print("Example vector (first 8 values):", embeddings[0][:8])