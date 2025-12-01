import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Page Config
st.set_page_config(page_title="Ecological Insights | Biodiversity Explorer", page_icon="🌿", layout="wide")

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

st.title("🌿 Ecological Insights")
st.markdown("Advanced metrics and seasonal patterns.")

# Diversity Metrics
st.subheader("Biodiversity Metrics")

# Calculate Shannon Index for the whole dataset (or filtered)
# H = -sum(pi * ln(pi))
def calculate_shannon_index(data):
    species_counts = data['scientificName'].value_counts()
    total = species_counts.sum()
    proportions = species_counts / total
    shannon_index = -sum(proportions * np.log(proportions))
    return shannon_index

# Calculate Simpson Index
# D = 1 - sum(pi^2)
def calculate_simpson_index(data):
    species_counts = data['scientificName'].value_counts()
    total = species_counts.sum()
    proportions = species_counts / total
    simpson_index = 1 - sum(proportions ** 2)
    return simpson_index

col1, col2 = st.columns(2)

with col1:
    shannon = calculate_shannon_index(df)
    st.metric("Shannon Diversity Index (H)", f"{shannon:.4f}", help="Higher value indicates higher diversity.")

with col2:
    simpson = calculate_simpson_index(df)
    st.metric("Simpson Diversity Index (1-D)", f"{simpson:.4f}", help="Measure of probability that two individuals randomly selected from a sample will belong to different species.")

st.markdown("---")

# Seasonality Radar Chart
st.subheader("🕰️ Seasonality Radar")
st.markdown("Observation frequency by month.")

# Aggregate by month
if 'month' in df.columns:
    month_counts = df['month'].value_counts().sort_index()
    # Ensure all months are present
    all_months = pd.Series(0, index=range(1, 13))
    month_counts = month_counts.combine(all_months, max, fill_value=0)
    
    # Radar Chart
    fig = go.Figure(data=go.Scatterpolar(
      r=month_counts.values,
      theta=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      fill='toself',
      line_color='#00f260'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, month_counts.max() * 1.1]
        ),
        bgcolor='rgba(0,0,0,0)'
      ),
      paper_bgcolor='rgba(0,0,0,0)',
      font=dict(color='white'),
      title="Seasonal Observation Pattern"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Month data not available.")

# Latitudinal Gradient
st.subheader("🌐 Latitudinal Gradient")
st.markdown("Species richness across latitudes.")

# Bin latitude
df['lat_bin'] = (df['decimalLatitude'] // 10) * 10
lat_richness = df.groupby('lat_bin')['scientificName'].nunique().reset_index()

fig2 = px.bar(lat_richness, x='lat_bin', y='scientificName',
              title="Species Richness by Latitude (10° Bins)",
              labels={'lat_bin': 'Latitude', 'scientificName': 'Unique Species Count'},
              color='scientificName', color_continuous_scale='Magma')

fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

st.plotly_chart(fig2, use_container_width=True)

# Latitudinal Distribution Boxplot
st.subheader("📦 Latitudinal Range by Kingdom")
st.markdown("Distribution of observations across latitudes for each kingdom.")

fig3 = px.box(df, x='kingdom', y='decimalLatitude', color='kingdom',
              title="Latitudinal Distribution by Kingdom",
              labels={'decimalLatitude': 'Latitude', 'kingdom': 'Kingdom'},
              color_discrete_sequence=px.colors.qualitative.Set3)

fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

st.plotly_chart(fig3, use_container_width=True)
