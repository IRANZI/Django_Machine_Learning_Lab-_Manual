import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Rwanda districts coordinates (approximate center points for visualization)
rwanda_districts = {
    'Kigali': {'lat': -1.9536, 'lon': 30.0605, 'province': 'Kigali City'},
    'Nyarugenge': {'lat': -1.9833, 'lon': 30.0589, 'province': 'Kigali City'},
    'Kicukiro': {'lat': -1.9444, 'lon': 30.1306, 'province': 'Kigali City'},
    'Gasabo': {'lat': -1.9167, 'lon': 30.1333, 'province': 'Kigali City'},
    'Northern': {'lat': -1.5, 'lon': 29.8, 'province': 'Northern Province'},
    'Musanze': {'lat': -1.5, 'lon': 29.6333, 'province': 'Northern Province'},
    'Burera': {'lat': -1.45, 'lon': 29.9833, 'province': 'Northern Province'},
    'Gicumbi': {'lat': -1.7333, 'lon': 30.05, 'province': 'Northern Province'},
    'Rulindo': {'lat': -1.6833, 'lon': 30.0167, 'province': 'Northern Province'},
    'Gakenke': {'lat': -1.6833, 'lon': 29.7167, 'province': 'Northern Province'},
    'Southern': {'lat': -2.3, 'lon': 29.6, 'province': 'Southern Province'},
    'Huye': {'lat': -2.6, 'lon': 29.75, 'province': 'Southern Province'},
    'Muhanga': {'lat': -2.2, 'lon': 29.7333, 'province': 'Southern Province'},
    'Nyanza': {'lat': -2.35, 'lon': 29.7167, 'province': 'Southern Province'},
    'Nyaruguru': {'lat': -2.75, 'lon': 29.6333, 'province': 'Southern Province'},
    'Gisagara': {'lat': -2.6167, 'lon': 29.8333, 'province': 'Southern Province'},
    'Ruhango': {'lat': -2.2167, 'lon': 29.7833, 'province': 'Southern Province'},
    'Kamonyi': {'lat': -2.0, 'lon': 29.9167, 'province': 'Southern Province'},
    'Nyamagabe': {'lat': -2.7833, 'lon': 29.5333, 'province': 'Southern Province'},
    'Eastern': {'lat': -1.6, 'lon': 30.4, 'province': 'Eastern Province'},
    'Ngoma': {'lat': -2.0833, 'lon': 30.4167, 'province': 'Eastern Province'},
    'Kirehe': {'lat': -2.2833, 'lon': 30.7, 'province': 'Eastern Province'},
    'Kayonza': {'lat': -1.95, 'lon': 30.35, 'province': 'Eastern Province'},
    'Rwamagana': {'lat': -2.0, 'lon': 30.4333, 'province': 'Eastern Province'},
    'Nyagatare': {'lat': -1.3, 'lon': 30.25, 'province': 'Eastern Province'},
    'Gatsibo': {'lat': -1.6, 'lon': 30.5, 'province': 'Eastern Province'},
    'Bugesera': {'lat': -2.1667, 'lon': 30.1, 'province': 'Eastern Province'},
    'Western': {'lat': -2.0, 'lon': 29.1, 'province': 'Western Province'},
    'Karongi': {'lat': -2.0, 'lon': 29.3833, 'province': 'Western Province'},
    'Rusizi': {'lat': -2.4667, 'lon': 29.0167, 'province': 'Western Province'},
    'Nyabihu': {'lat': -1.5167, 'lon': 29.5, 'province': 'Western Province'},
    'Ngororero': {'lat': -1.8833, 'lon': 29.6167, 'province': 'Western Province'},
    'Rubavu': {'lat': -1.4833, 'lon': 29.2333, 'province': 'Western Province'},
    'Rutsiro': {'lat': -1.8833, 'lon': 29.3333, 'province': 'Western Province'},
    'Nyamasheke': {'lat': -2.2167, 'lon': 29.05, 'province': 'Western Province'},
}

def create_rwanda_map(df):
    """Create an interactive map showing vehicle clients by district"""
    
    # Count clients by district
    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']
    
    # Merge with district coordinates
    lat_list = []
    lon_list = []
    province_list = []
    
    for district_name in district_counts['district']:
        if district_name in rwanda_districts:
            lat_list.append(rwanda_districts[district_name]['lat'])
            lon_list.append(rwanda_districts[district_name]['lon'])
            province_list.append(rwanda_districts[district_name]['province'])
        else:
            lat_list.append(-2.0)  # Default center of Rwanda
            lon_list.append(30.0)
            province_list.append('Unknown')
    
    district_counts['lat'] = lat_list
    district_counts['lon'] = lon_list
    district_counts['province'] = province_list
    
    # Create map
    fig = px.scatter_mapbox(
        district_counts,
        lat="lat",
        lon="lon",
        color="client_count",
        size="client_count",
        hover_name="district",
        hover_data={
            "client_count": True,
            "province": True
        },
        color_continuous_scale="Viridis",
        size_max=30,
        zoom=7,
        center={"lat": -1.9536, "lon": 30.0605},
        mapbox_style="open-street-map",
        title="Vehicle Clients Distribution by District in Rwanda"
    )
    
    # Customize map
    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title={
            'text': "Vehicle Clients Distribution by District in Rwanda",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        }
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
