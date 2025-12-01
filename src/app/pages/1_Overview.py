import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Config
st.set_page_config(page_title="Overview | Biodiversity Explorer", page_icon="📊", layout="wide")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
local_css(css_path)

# Data Loading
@st.cache_data
def load_data():
    # Adjust path to point to the cleaned dataset relative to this file
    # This file is in src/app/pages/, data is in data/cleaned_dataset.csv
    # So we go up 3 levels: pages -> app -> src -> root -> data
    # Actually: src/app/pages/../../.. -> root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_path = os.path.join(root_dir, "data", "cleaned_dataset.csv")
    
    if not os.path.exists(data_path):
        st.error(f"Data file not found at: {data_path}")
        return pd.DataFrame()
        
    df = pd.read_csv(data_path)
    return df

df = load_data()

if df.empty:
    st.stop()

# Header
st.title("📊 Project Overview")
st.markdown("High-level metrics and temporal trends of the biodiversity dataset.")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Observations", f"{len(df):,}")

with col2:
    species_count = df['scientificName'].nunique()
    st.metric("Unique Species", f"{species_count:,}")

with col3:
    # Assuming 'countryCode' or similar exists, otherwise use 'kingdom'
    if 'countryCode' in df.columns:
        loc_count = df['countryCode'].nunique()
        label = "Countries"
    else:
        loc_count = df['kingdom'].nunique()
        label = "Kingdoms"
    st.metric(label, loc_count)

with col4:
    # Time range
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    st.metric("Time Range", f"{min_year} - {max_year}")

st.markdown("---")

# Temporal Analysis
st.subheader("📈 Observations Over Time")

# Aggregate by year
year_counts = df['year'].value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']

# Interactive Line Chart
fig = px.area(year_counts, x='Year', y='Count', 
              title='Growth of Biodiversity Observations',
              markers=True,
              color_discrete_sequence=['#00f260'])

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
)

st.plotly_chart(fig, use_container_width=True)

# Quick Kingdom Breakdown
st.subheader("👑 Kingdom Distribution")
kingdom_counts = df['kingdom'].value_counts().reset_index()
kingdom_counts.columns = ['Kingdom', 'Count']

fig2 = px.bar(kingdom_counts, x='Count', y='Kingdom', orientation='h',
             color='Count', color_continuous_scale='Viridis',
             title="Observations by Kingdom")

fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig2, use_container_width=True)
