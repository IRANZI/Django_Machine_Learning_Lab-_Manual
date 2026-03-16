import pandas as pd
import json
import plotly.graph_objects as go
import plotly.io as pio


def get_rwanda_map(df):
    district_counts = df["district"].value_counts().reset_index()
    district_counts.columns = ["district", "client_count"]

    with open("dummy-data/rwanda_districts.geojson", "r", encoding="utf-8") as f:
        rwanda_geojson = json.load(f)

    # Build centroid list from geojson so text can be placed on districts
    label_rows = []
    for feature in rwanda_geojson["features"]:
        district_name = feature["properties"]["NAME_2"]
        geometry = feature["geometry"]

        coords = []
        if geometry["type"] == "Polygon":
            coords = geometry["coordinates"][0]
        elif geometry["type"] == "MultiPolygon":
            largest_polygon = max(geometry["coordinates"], key=lambda poly: len(poly[0]))
            coords = largest_polygon[0]

        if not coords:
            continue

        lons = [pt[0] for pt in coords]
        lats = [pt[1] for pt in coords]
        centroid_lon = sum(lons) / len(lons)
        centroid_lat = sum(lats) / len(lats)

        match = district_counts[district_counts["district"] == district_name]
        client_count = int(match["client_count"].iloc[0]) if not match.empty else 0

        label_rows.append(
            {
                "district": district_name,
                "client_count": client_count,
                "lon": centroid_lon,
                "lat": centroid_lat,
                "label": f"{district_name}<br>{client_count}",
            }
        )

    labels_df = pd.DataFrame(label_rows)

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=rwanda_geojson,
            locations=district_counts["district"],
            z=district_counts["client_count"],
            featureidkey="properties.NAME_2",
            colorscale="Viridis",
            colorbar_title="Number of Clients",
            marker_line_width=0.5,
            marker_line_color="white",
            hovertemplate="<b>%{location}</b><br>Clients: %{z}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scattergeo(
            lon=labels_df["lon"],
            lat=labels_df["lat"],
            text=labels_df["label"],
            mode="text",
            textfont=dict(size=9, color="black"),
            hoverinfo="skip",
        )
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title="Vehicle Clients per District in Rwanda",
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )

    return pio.to_html(fig, full_html=False)
# Data Exploration
def dataset_exploration(df):
  table_html = df.head().to_html(
  classes="table table-bordered table-striped table-sm",
  float_format="%.2f",
  justify="center",
  index=False,
  )
  return table_html
# Data description
def data_exploration(df):
  table_html = df.head().to_html(
  classes="table table-bordered table-striped table-sm",
  float_format="%.2f",
  justify="center",
  )
  return table_html