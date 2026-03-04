# ============================================================
# Step 5 — Semantic Search (+ optional Geospatial Filtering)
#
# Goal
# ----
# Build a reusable function that:
#   1) Converts a user query into an embedding vector
#   2) Uses the FAISS index to retrieve the most similar murals
#   3) Returns a clean results table with scores + mural details
#   4) (Optional) Filters results by distance from a lat/lon point
#
# Inputs this step expects (from Steps 3 & 4):
# ------------------------------------------
#   - embed_model: SentenceTransformer model loaded in Step 3
#   - index:       FAISS index built in Step 4 (IndexFlatIP)
#   - meta_df:     Metadata DataFrame aligned to embeddings/index rows
#
# Key idea
# --------
# - We normalized embeddings (unit length) in Step 3.
# - We built an IndexFlatIP index (inner product) in Step 4.
# - For normalized vectors, inner product behaves like cosine similarity:
#     higher score = more semantically similar
# ============================================================

import numpy as np
import pandas as pd
from math import radians, sin, cos, asin, sqrt

# ------------------------------------------------------------
# (A) Geo utility: Haversine distance (miles)
#
# Why not geopy?
# - geopy is fine, but haversine avoids extra dependencies and is fast.
#
# Note:
# - This computes great-circle distance on Earth (good enough for miles radius filtering).
# ------------------------------------------------------------
def haversine_miles(lat1, lon1, lat2, lon2):
    """Return distance in miles between two (lat, lon) points."""
    # Earth radius in miles
    R = 3958.7613

    # Convert degrees -> radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


# ------------------------------------------------------------
# (B) Semantic search function
#
# Parameters (most important):
# - query: Natural language string from the user
# - k:     How many "nearest neighbors" to retrieve from FAISS
#
# Optional geo parameters:
# - center_lat, center_lon: "search around here"
# - radius_miles: filter to only those within this radius
#
# Practical guidance:
# - If you want geo filtering, retrieve a bigger k first (e.g. k=50),
#   then filter down by radius and re-rank as needed.
# ------------------------------------------------------------
def semantic_search(
    query: str,
    k: int = 10,
    *,
    center_lat: float | None = None,
    center_lon: float | None = None,
    radius_miles: float | None = None,
    min_score: float | None = None,
) -> pd.DataFrame:
    """
    Perform semantic search over murals, optionally constrained by a geographic radius.

    Returns a DataFrame with:
      - rank:             1..N
      - score:            similarity score (higher is better; cosine-like)
      - distance_miles:   if geo filter enabled, computed distance from center
      - mural_id, title, artist, community_area, latitude, longitude, search_text
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")

    if k <= 0:
        raise ValueError("k must be a positive integer")

    # --- 1) Embed the query text ---
    # We normalize the query embedding so that inner product ~ cosine similarity,
    # matching how we built the FAISS index.
    q_vec = embed_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    # --- 2) Search FAISS ---
    # distances here are inner-product scores (not Euclidean distance)
    # For normalized embeddings, higher score means "more similar."
    scores, idxs = index.search(q_vec, k)

    scores = scores[0]   # shape: (k,)
    idxs = idxs[0]       # shape: (k,)

    # Guard: FAISS can return -1 indices in some edge cases
    valid = idxs >= 0
    scores = scores[valid]
    idxs = idxs[valid]

    # --- 3) Build results table by joining indices to metadata ---
    results = meta_df.iloc[idxs].copy()
    results.insert(0, "score", scores)

    # Optional: apply a minimum similarity threshold
    if min_score is not None:
        results = results[results["score"] >= float(min_score)].copy()

    # --- 4) Optional geo filtering ---
    # If center + radius provided, compute distance and filter.
    if center_lat is not None and center_lon is not None and radius_miles is not None:
        center_lat = float(center_lat)
        center_lon = float(center_lon)
        radius_miles = float(radius_miles)

        # Compute distance for each row
        results["distance_miles"] = results.apply(
            lambda r: haversine_miles(center_lat, center_lon, r["latitude"], r["longitude"]),
            axis=1,
        )

        # Keep only murals within the requested radius
        results = results[results["distance_miles"] <= radius_miles].copy()

        # Optional: re-rank within the radius using score first, then nearest distance
        results = results.sort_values(["score", "distance_miles"], ascending=[False, True])

    else:
        # If no geo filter, just rank by semantic similarity score
        results = results.sort_values("score", ascending=False)

    # --- 5) Add rank + a few convenience columns ---
    results = results.reset_index(drop=True)
    results.insert(0, "rank", results.index + 1)

    # Include the query in the output (helpful when you start saving results for OAC)
    results.insert(1, "query", query)

    # Ensure consistent column order for downstream visualization and export
    ordered_cols = [
        "rank", "query", "score",
        # distance_miles only exists when geo filtering is enabled
        *([ "distance_miles" ] if "distance_miles" in results.columns else []),
        "mural_id", "title", "artist", "community_area",
        "latitude", "longitude",
        "search_text",
    ]
    results = results[ordered_cols]

    return results


# ============================================================
# Quick test runs
# ============================================================

# 1) Pure semantic search (no geo filter)
semantic_search("murals about civil rights and activism", k=10).head(10)

# 2) Semantic search + geo filter around downtown Chicago (example coords)
# Note: We retrieve more results first (k=50) then filter down to those within radius.
semantic_search(
    "music and jazz themes",
    k=50,
    center_lat=41.8781,     # downtown Chicago-ish
    center_lon=-87.6298,
    radius_miles=3.0,
).head(10)