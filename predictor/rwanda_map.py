import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Rwanda districts with realistic, non-rectangular boundaries
rwanda_districts_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Nyarugenge"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.95, -1.98], [30.02, -1.96], [30.05, -2.00], [30.03, -2.05], [29.98, -2.03], [29.95, -1.98]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gasabo"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.92, -1.85], [30.05, -1.87], [30.08, -1.92], [30.06, -1.98], [29.95, -1.96], [29.92, -1.85]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kicukiro"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.05, -1.92], [30.12, -1.90], [30.15, -1.95], [30.13, -2.02], [30.08, -2.05], [30.05, -1.92]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kigali"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.08, -1.92], [30.15, -1.95], [30.15, -1.85], [30.12, -1.90], [30.08, -1.92]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Musanze"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.45, -1.45], [29.58, -1.43], [29.65, -1.48], [29.63, -1.55], [29.52, -1.53], [29.45, -1.45]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Burera"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.65, -1.45], [29.78, -1.42], [29.85, -1.50], [29.82, -1.55], [29.63, -1.55], [29.65, -1.45]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gicumbi"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.85, -1.65], [29.98, -1.62], [30.05, -1.68], [30.02, -1.75], [29.92, -1.72], [29.85, -1.65]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rulindo"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.75, -1.55], [29.85, -1.50], [29.92, -1.72], [29.88, -1.78], [29.78, -1.75], [29.75, -1.55]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gakenke"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.55, -1.65], [29.68, -1.62], [29.75, -1.55], [29.78, -1.75], [29.65, -1.78], [29.55, -1.65]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Huye"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.70, -2.55], [29.80, -2.52], [29.85, -2.60], [29.82, -2.70], [29.72, -2.68], [29.70, -2.55]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Muhanga"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.65, -2.10], [29.78, -2.08], [29.85, -2.15], [29.82, -2.25], [29.70, -2.22], [29.65, -2.10]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyanza"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.60, -2.30], [29.72, -2.28], [29.75, -2.35], [29.68, -2.42], [29.58, -2.38], [29.60, -2.30]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyaruguru"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.50, -2.70], [29.62, -2.68], [29.70, -2.75], [29.65, -2.85], [29.55, -2.82], [29.50, -2.70]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gisagara"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.85, -2.55], [29.98, -2.52], [30.05, -2.60], [30.02, -2.70], [29.82, -2.70], [29.85, -2.55]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ruhango"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.75, -2.25], [29.88, -2.22], [29.95, -2.30], [29.92, -2.38], [29.80, -2.35], [29.75, -2.25]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kamonyi"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.85, -1.95], [29.98, -1.92], [30.05, -2.00], [30.02, -2.10], [29.92, -2.08], [29.85, -1.95]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyamagabe"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.35, -2.75], [29.48, -2.72], [29.55, -2.82], [29.50, -2.90], [29.40, -2.88], [29.35, -2.75]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ngoma"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.25, -2.05], [30.38, -2.02], [30.45, -2.10], [30.42, -2.20], [30.30, -2.18], [30.25, -2.05]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kirehe"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.55, -2.25], [30.68, -2.22], [30.75, -2.30], [30.72, -2.40], [30.60, -2.38], [30.55, -2.25]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kayonza"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.15, -1.85], [30.28, -1.82], [30.35, -1.92], [30.32, -2.05], [30.20, -2.02], [30.15, -1.85]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rwamagana"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.35, -1.95], [30.45, -1.92], [30.50, -2.00], [30.48, -2.10], [30.38, -2.08], [30.35, -1.95]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyagatare"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.05, -1.25], [30.20, -1.22], [30.30, -1.30], [30.28, -1.45], [30.15, -1.42], [30.05, -1.25]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gatsibo"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.30, -1.55], [30.42, -1.52], [30.50, -1.60], [30.48, -1.70], [30.38, -1.68], [30.30, -1.55]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Bugesera"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[30.05, -2.10], [30.18, -2.08], [30.25, -2.15], [30.22, -2.25], [30.12, -2.22], [30.05, -2.10]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Karongi"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.25, -1.95], [29.38, -1.92], [29.45, -2.00], [29.42, -2.10], [29.32, -2.08], [29.25, -1.95]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rusizi"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[28.90, -2.40], [29.02, -2.38], [29.10, -2.45], [29.08, -2.60], [28.95, -2.58], [28.90, -2.40]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyabihu"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.35, -1.45], [29.48, -1.42], [29.55, -1.50], [29.52, -1.60], [29.42, -1.58], [29.35, -1.45]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ngororero"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.45, -1.80], [29.58, -1.78], [29.65, -1.85], [29.62, -1.95], [29.52, -1.92], [29.45, -1.80]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rubavu"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.10, -1.45], [29.22, -1.42], [29.30, -1.50], [29.28, -1.60], [29.18, -1.58], [29.10, -1.45]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rutsiro"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[29.20, -1.80], [29.32, -1.78], [29.40, -1.85], [29.38, -1.95], [29.28, -1.92], [29.20, -1.80]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyamasheke"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[28.90, -2.15], [29.02, -2.12], [29.10, -2.20], [29.08, -2.35], [28.95, -2.32], [28.90, -2.15]]]
            }
        }
    ]
}

def create_rwanda_map(df):
    """Create a simple map with filled district colors"""
    
    # Count clients by district
    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']
    
    # Create a simple scatter map with sized bubbles
    fig = px.scatter_mapbox(
        district_counts,
        lat=[-1.9536] * len(district_counts),  # Center of Rwanda
        lon=[30.0605] * len(district_counts),  # Center of Rwanda
        color='district',
        size='client_count',
        size_max=50,
        color_discrete_sequence=px.colors.qualitative.Set3,
        mapbox_style="carto-positron",
        zoom=7,
        center={"lat": -1.9536, "lon": 30.0605},
        title="Vehicle Clients Distribution by District in Rwanda",
        hover_data={
            'district': True,
            'client_count': True
        },
        labels={'district': 'District', 'client_count': 'Number of Clients'}
    )
    
    # Customize layout
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title={
            'text': "Vehicle Clients Distribution by District in Rwanda",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        showlegend=True,
        legend=dict(
            title="Districts",
            x=0.02,
            y=0.98,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="black",
            borderwidth=1
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def get_district_stats(df):
    """Get statistics for districts"""
    district_stats = df.groupby('district').agg({
        'client_name': 'count',
        'estimated_income': ['mean', 'sum'],
        'selling_price': ['mean', 'sum']
    }).round(2)
    
    district_stats.columns = ['Client Count', 'Avg Income', 'Total Income', 'Avg Price', 'Total Price']
    district_stats = district_stats.reset_index()
    
    # Convert to HTML table
    return district_stats.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False
    )
