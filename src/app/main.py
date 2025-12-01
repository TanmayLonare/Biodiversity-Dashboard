import streamlit as st
from streamlit_option_menu import option_menu
import os

# Page Config
st.set_page_config(
    page_title="Biodiversity Explorer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(__file__), "style.css")
local_css(css_path)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/leaf.png", width=60)
    st.title("Biodiversity\nExplorer")
    
    st.info("Navigate through the pages above to explore the dataset.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Settings")
    theme = st.select_slider("Theme Intensity", options=["Soft", "Deep", "Midnight"], value="Deep")
    


# Landing Page Content (if no page selected, though Streamlit handles pages automatically)
st.title("🌍 Global Biodiversity Dashboard")
st.markdown("""
### Welcome to the Premium Biodiversity Explorer

This dashboard provides a deep dive into global biodiversity data, featuring:
- **Taxonomic Analysis**: Explore the hierarchy of life.
- **Geospatial Intelligence**: Interactive heatmaps and distribution analysis.
- **Ecological Metrics**: Understanding diversity and seasonality.

**👈 Select a page from the sidebar to get started.**
""")

# Add a cool hero image or animation if possible (using standard streamlit elements for now)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Data Source", value="GBIF", delta="Verified")
with col2:
    st.metric(label="Status", value="Live", delta="Online")
with col3:
    st.metric(label="Version", value="1.0.0", delta_color="off")
