# ============================================================
# Step 1 — Load Chicago Murals data (Socrata / SODA API)
#
# This notebook example uses the public, no-auth SODA2 endpoint:
#   https://data.cityofchicago.org/resource/we8h-apcf.json
#
# Why API?
# - No manual downloads
# - Always pulls the latest published data
# - Easy to reproduce
#
# If you prefer a CSV instead (common in enterprise workflows):
# - Download/export the dataset as CSV and store it in Object Storage
# - Then use: pd.read_csv("path/to/file.csv")
# - Or download from a CSV URL: pd.read_csv("https://.../file.csv")
# ============================================================

import requests
import pandas as pd

SODA_ENDPOINT = "https://data.cityofchicago.org/resource/we8h-apcf.json"

def fetch_soda_all(
    endpoint: str,
    select: str | None = None,
    where: str | None = None,
    order: str | None = None,
    limit: int = 5000,
    max_rows: int | None = None,
    timeout: int = 30,
) -> pd.DataFrame:
    """
    Fetch all rows from a Socrata SODA endpoint using pagination ($limit/$offset).

    Parameters
    ----------
    endpoint : str
        The SODA endpoint ending in .json
    select, where, order : str | None
        Optional SoQL clauses to reduce payload and control results.
        Example select: "id, title, artist, description, latitude, longitude"
    limit : int
        Page size. Socrata commonly allows up to 50,000 but 5,000 is a safe default.
    max_rows : int | None
        Optional cap for quick tests.
    timeout : int
        HTTP timeout seconds.

    Returns
    -------
    pd.DataFrame
        All retrieved rows.
    """
    offset = 0
    rows = []

    while True:
        params = {"$limit": limit, "$offset": offset}
        if select:
            params["$select"] = select
        if where:
            params["$where"] = where
        if order:
            params["$order"] = order

        resp = requests.get(endpoint, params=params, timeout=timeout)
        resp.raise_for_status()

        batch = resp.json()
        if not batch:
            break

        rows.extend(batch)
        offset += limit

        if max_rows is not None and len(rows) >= max_rows:
            rows = rows[:max_rows]
            break

    return pd.DataFrame(rows)

# Optional: reduce payload by selecting only fields you care about.
# If you're not sure of the exact column names yet, start with select=None.
df_raw = fetch_soda_all(
    endpoint=SODA_ENDPOINT,
    select=None,          # Example: "title,description,latitude,longitude"
    where=None,           # Example: "latitude IS NOT NULL AND longitude IS NOT NULL"
    order=None,           # Example: "title ASC"
    limit=5000,
)

print("Rows:", len(df_raw))
print("Columns:", list(df_raw.columns))
df_raw.head()