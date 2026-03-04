# ------------------------------------------------------------
# (B) MAP VIEW (Folium)
#
# Folium renders interactive Leaflet maps directly in notebooks.
# We'll:
# - Center map on the query location (if provided)
# - Add markers for each returned mural
# - Include popup text with rank/title/score (+distance)
# ------------------------------------------------------------

%pip -q install folium
import folium

# Choose a center point:
# - If you used geo filtering, center on that point
# - Otherwise center on the average of the result set
if "distance_miles" in results_df.columns and len(results_df) > 0:
    center_lat = 41.8781
    center_lon = -87.6298
else:
    center_lat = results_df["latitude"].mean()
    center_lon = results_df["longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Optional: mark the center point used for radius filtering
folium.Marker(
    [center_lat, center_lon],
    popup="Search Center",
    tooltip="Search Center",
).add_to(m)

# Add each mural as a marker
for _, row in results_df.iterrows():
    popup_lines = [
        f"Rank: {row['rank']}",
        f"Title: {row['title']}",
        f"Score: {row['score']:.4f}",
    ]
    if "distance_miles" in row:
        # if distance_miles exists, show it (it will if geo filter was used)
        if pd.notna(row.get("distance_miles", None)):
            popup_lines.append(f"Distance: {row['distance_miles']:.2f} miles")

    popup_text = "<br>".join(popup_lines)

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"{row['rank']}. {row['title']}",
    ).add_to(m)

m