# ============================================================
# Step 2 — Normalize Source Schema to AI-Ready Schema
#
# Why are we doing this?
# -----------------------
# We want to standardize the dataset into a consistent internal format
# so that downstream embedding + geo logic does not depend on the
# original dataset column names.
#
# We are NOT altering the meaning of the data.
# We are simply:
#   - Renaming columns to canonical names
#   - Ensuring latitude/longitude are numeric
#   - Creating a unified text field for embeddings
# ============================================================

df_norm = df_raw.copy()

# --- 1️⃣ Rename columns to canonical internal names ---
df_norm = df_norm.rename(columns={
    "mural_registration_id": "mural_id",
    "artist_credit": "artist",
    "artwork_title": "title",
    "description_of_artwork": "description",
    "community_areas": "community_area"
})

# --- 2️⃣ Ensure numeric latitude / longitude ---
df_norm["latitude"] = pd.to_numeric(df_norm["latitude"], errors="coerce")
df_norm["longitude"] = pd.to_numeric(df_norm["longitude"], errors="coerce")

# --- 3️⃣ Drop rows missing coordinates (required for geo filtering) ---
df_norm = df_norm.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)

# --- 4️⃣ Create unified text field for embeddings ---
# Why?
# Embedding models work best when given a coherent text block.
# We combine title + description + location for better context.

df_norm["search_text"] = (
    df_norm["title"].fillna("") + " " +
    df_norm["description"].fillna("") + " " +
    df_norm["location_description"].fillna("")
).str.strip()

print("Normalized columns:")
print(df_norm.columns.tolist())

df_norm.head()