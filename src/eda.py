

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Settings
plt.style.use('ggplot')
FIG_DIR = r'c:\Users\ASUS\Desktop\Biodiversity\reports\figures'
os.makedirs(FIG_DIR, exist_ok=True)

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_taxonomic_distribution(df):
    print("Plotting taxonomic distribution...")
    # Kingdom count
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='kingdom', order=df['kingdom'].value_counts().index, palette='viridis')
    plt.title('Distribution of Observations by Kingdom')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'kingdom_distribution.png'))
    plt.close()

    # Top 10 Phyla
    top_phyla = df['phylum'].value_counts().head(10).index
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df[df['phylum'].isin(top_phyla)], y='phylum', order=top_phyla, palette='magma')
    plt.title('Top 10 Phyla by Observation Count')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'top_10_phyla.png'))
    plt.close()

def plot_temporal_trends(df):
    print("Plotting temporal trends...")
    # Observations by Year
    year_counts = df['year'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    year_counts.plot(kind='line', marker='o')
    plt.title('Observations over Time (Year)')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'observations_by_year.png'))
    plt.close()

    # Observations by Month
    month_counts = df['month'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=month_counts.index, y=month_counts.values, palette='coolwarm')
    plt.title('Seasonal Distribution of Observations')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'observations_by_month.png'))
    plt.close()

def plot_geographical_distribution(df):
    print("Plotting geographical distribution...")
    # Simple scatter plot of lat/lon
    plt.figure(figsize=(15, 10))
    plt.scatter(df['decimalLongitude'], df['decimalLatitude'], alpha=0.1, s=1, c=df['decimalLongitude'], cmap='twilight')
    plt.title('Global Distribution of Observations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'global_map_static.png'))
    plt.close()
    
    # Plotly interactive map
    try:
        # Sample for performance
        sample_size = min(10000, len(df))
        print(f"Sampling {sample_size} points for interactive map...")
        sample_df = df.sample(sample_size)
        fig = px.scatter_geo(sample_df, lat='decimalLatitude', lon='decimalLongitude', 
                             color='kingdom', hover_name='scientificName',
                             title='Sampled Observations Distribution')
        fig.write_html(os.path.join(FIG_DIR, 'interactive_map.html'))
    except Exception as e:
        print(f"Could not create interactive map: {e}")

def plot_latitudinal_distribution(df):
    print("Plotting latitudinal distribution (Boxplot)...")
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='kingdom', y='decimalLatitude', palette='Set3')
    plt.title('Latitudinal Distribution by Kingdom')
    plt.ylabel('Latitude')
    plt.xlabel('Kingdom')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'latitude_boxplot.png'))
    plt.savefig(os.path.join(FIG_DIR, 'latitude_boxplot.png'))
    plt.close()

def plot_seasonal_heatmap(df):
    print("Plotting seasonal heatmap...")
    # Filter for recent years to keep heatmap readable
    recent_df = df[df['year'] >= 2010]
    heatmap_data = pd.crosstab(recent_df['year'], recent_df['month'])
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d')
    plt.title('Observation Intensity (Year vs Month) - Post 2010')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'seasonal_heatmap.png'))
    plt.close()

def plot_phylum_violin(df):
    print("Plotting phylum violin plot...")
    top_phyla = df['phylum'].value_counts().head(5).index
    filtered_df = df[df['phylum'].isin(top_phyla)]
    
    plt.figure(figsize=(14, 8))
    sns.violinplot(data=filtered_df, x='phylum', y='decimalLatitude', palette='muted')
    plt.title('Latitudinal Distribution of Top 5 Phyla (Violin Plot)')
    plt.xlabel('Phylum')
    plt.ylabel('Latitude')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'phylum_violin.png'))
    plt.close()

def main():
    input_file = r"c:\Users\ASUS\Desktop\Biodiversity\data\cleaned_dataset.csv"
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    df = load_data(input_file)
    print(f"Loaded {len(df)} records.")

    plot_taxonomic_distribution(df)
    plot_temporal_trends(df)
    plot_geographical_distribution(df)
    plot_latitudinal_distribution(df)
    plot_seasonal_heatmap(df)
    plot_phylum_violin(df)

    
    print(f"EDA complete. Figures saved to {FIG_DIR}")

if __name__ == "__main__":
    main()
