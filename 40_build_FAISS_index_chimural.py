# ============================================================
# Step 4 — Build a FAISS Vector Index
#
# Input:
#   embeddings: numpy array (num_rows, dim) from Step 3
#
# Why FAISS?
#   FAISS gives fast nearest-neighbor search over vectors.
#
# Why IndexFlatIP?
#   - We normalized embeddings (unit length)
#   - Inner product then behaves like cosine similarity
# ============================================================

%pip -q install faiss-cpu
import numpy as np
import faiss

# Ensure float32 (FAISS expects float32)
embeddings_f32 = embeddings.astype("float32")

dim = embeddings_f32.shape[1]
index = faiss.IndexFlatIP(dim)  # cosine-like when embeddings are normalized
index.add(embeddings_f32)

print("✅ FAISS index built")
print("Vectors in index:", index.ntotal)
print("Vector dimension:", dim)

# ============================================================
# Create a compact metadata table used to interpret search results.
# FAISS returns integer positions -> we map those back to mural_id, title, coords, etc.
# ============================================================

meta_cols = ["mural_id", "title", "artist", "community_area", "latitude", "longitude", "search_text"]
meta_df = df_norm[meta_cols].copy()

print("Metadata rows:", len(meta_df))
meta_df.head()

# ============================================================
# Create a compact metadata table used to interpret search results.
# FAISS returns integer positions -> we map those back to mural_id, title, coords, etc.
# ============================================================

meta_cols = ["mural_id", "title", "artist", "community_area", "latitude", "longitude", "search_text"]
meta_df = df_norm[meta_cols].copy()

print("Metadata rows:", len(meta_df))
meta_df.head()

# ============================================================
# Persist index and metadata locally
# ============================================================

INDEX_PATH = "chicago_murals.faiss"
META_PATH  = "chicago_murals_meta.parquet"  # parquet is compact; CSV is also fine

faiss.write_index(index, INDEX_PATH)
meta_df.to_parquet(META_PATH, index=False)

print("✅ Saved locally:")
print(" -", INDEX_PATH)
print(" -", META_PATH)