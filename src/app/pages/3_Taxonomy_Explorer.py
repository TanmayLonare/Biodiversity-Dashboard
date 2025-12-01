import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Config
st.set_page_config(page_title="Taxonomy | Biodiversity Explorer", page_icon="🧬", layout="wide")

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

st.title("🧬 Taxonomy Explorer")
st.markdown("Visualize the hierarchical structure of the observed species.")

# Sunburst Chart
st.subheader("Interactive Taxonomic Hierarchy")
st.markdown("Click on a sector to zoom in. (Kingdom -> Phylum -> Class)")

# Prepare data for Sunburst
# We need to handle missing values for the hierarchy to work
sunburst_cols = ['kingdom', 'phylum', 'class']
sunburst_df = df[sunburst_cols].dropna()

# Group by hierarchy
sunburst_data = sunburst_df.groupby(sunburst_cols).size().reset_index(name='count')

# Limit to top N for performance if needed, but sunburst handles reasonable size well
if len(sunburst_data) > 1000:
    st.info("Aggregating data for better visualization performance...")
    sunburst_data = sunburst_data.sort_values('count', ascending=False).head(500)

fig = px.sunburst(sunburst_data, path=['kingdom', 'phylum', 'class'], values='count',
                  color='count', color_continuous_scale='RdBu',
                  title="Taxonomic Sunburst")

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    margin=dict(t=30, l=0, r=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# Treemap
st.subheader("Top Species Treemap")
st.markdown("Size represents the number of observations.")

# Top 50 Species
top_species = df['scientificName'].value_counts().head(50).reset_index()
top_species.columns = ['scientificName', 'count']

# Merge back kingdom info for color
species_kingdom = df[['scientificName', 'kingdom']].drop_duplicates().set_index('scientificName')
top_species = top_species.join(species_kingdom, on='scientificName')

fig2 = px.treemap(top_species, path=['kingdom', 'scientificName'], values='count',
                  color='kingdom',
                  title="Top 50 Most Observed Species")

fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    margin=dict(t=30, l=0, r=0, b=0)
)

st.plotly_chart(fig2, use_container_width=True)
