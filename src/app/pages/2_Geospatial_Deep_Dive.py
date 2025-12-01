import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Config
st.set_page_config(page_title="Geospatial | Biodiversity Explorer", page_icon="🌍", layout="wide")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
local_css(css_path)

# Data Loading
@st.cache_data
def load_data():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_path = os.path.join(root_dir, "data", "cleaned_dataset.csv")
    if not os.path.exists(data_path):
        return pd.DataFrame()
    return pd.read_csv(data_path)

df = load_data()

st.title("🌍 Geospatial Deep Dive")
st.markdown("Explore the global distribution of species with interactive maps.")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    
    # Kingdom Filter
    kingdoms = ['All'] + sorted(df['kingdom'].unique().tolist())
    selected_kingdom = st.selectbox("Select Kingdom", kingdoms)
    
    # Year Filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    selected_year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Apply Filters
filtered_df = df.copy()
if selected_kingdom != 'All':
    filtered_df = filtered_df[filtered_df['kingdom'] == selected_kingdom]

filtered_df = filtered_df[
    (filtered_df['year'] >= selected_year_range[0]) & 
    (filtered_df['year'] <= selected_year_range[1])
]

st.info(f"Showing {len(filtered_df):,} observations.")

import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster

# Map Visualization
st.subheader("Global Interactive Map (Folium)")
st.markdown("Explore biodiversity hotspots with this interactive map.")

if len(filtered_df) > 0:
    # Center map on the mean coordinates
    center_lat = filtered_df['decimalLatitude'].mean()
    center_lon = filtered_df['decimalLongitude'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2, tiles="cartodbdark_matter")
    
    # Heatmap Layer
    heat_data = [[row['decimalLatitude'], row['decimalLongitude']] for index, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=15, blur=10).add_to(m)
    
    # Marker Cluster Layer (for smaller datasets or sampled)
    if len(filtered_df) < 5000:
        marker_cluster = MarkerCluster().add_to(m)
        for idx, row in filtered_df.iterrows():
            folium.Marker(
                location=[row['decimalLatitude'], row['decimalLongitude']],
                popup=f"{row['scientificName']} ({row['kingdom']})",
                tooltip=row['scientificName']
            ).add_to(marker_cluster)
    else:
        st.info("Dataset too large for individual markers. Showing Heatmap only.")

    st_folium(m, width=1000, height=600)
else:
    st.warning("No data available for the selected filters.")

# Hexbin Map (Alternative View)
st.subheader("📍 Regional Clusters")
st.markdown("Aggregated view of observations by region.")

if len(filtered_df) > 0:
    # Sample for performance if needed
    if len(filtered_df) > 20000:
        map_df = filtered_df.sample(20000)
    else:
        map_df = filtered_df

    fig2 = px.scatter_geo(map_df, lat='decimalLatitude', lon='decimalLongitude',
                          color='kingdom',
                          projection="natural earth",
                          title="Observation Clusters",
                          opacity=0.6)
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showland=True, landcolor="#2c3e50",
            showocean=True, oceancolor="#1a252f"
        ),
        font=dict(color='white')
    )
    st.plotly_chart(fig2, use_container_width=True)
