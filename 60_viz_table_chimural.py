# ============================================================
# Step 6 — Visualize Results (Table + Map)
#
# Goal
# ----
# After Step 5 returns a results DataFrame, we want a clean visualization:
#   1) A readable table for quick inspection (rank, title, score, distance)
#   2) A map showing the returned murals by latitude/longitude
#
# Why this matters
# ---------------
# - In real business workflows, the "AI result" isn't useful until it is
#   presented in a human-friendly way (tables, maps, dashboards).
# - This is the bridge between "model output" and "stakeholder value."
#
# Inputs expected
# --------------
# - results_df from semantic_search(...)
# ============================================================

%pip -q install folium
import pandas as pd

# Run a search (pick one of these or create your own)
results_df = semantic_search(
    "plants and animals",
    k=50,
    center_lat=41.8781,
    center_lon=-87.6298,
    radius_miles=3.0,
)

# ------------------------------------------------------------
# (A) TABLE VIEW
# ------------------------------------------------------------
# We'll display a compact table that is easy to scan.
table_cols = [
    "rank", "title", "artist", "community_area", "score", "search_text"
]
if "distance_miles" in results_df.columns:
    table_cols.insert(4, "distance_miles")

display(
    results_df[table_cols].head(5)
)