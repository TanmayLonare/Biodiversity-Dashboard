# Biodiversity Data Analysis Project

## Author
**Name:** Tanmay Lonare  
**Roll No:** MT2405  
**Subject:** Advance Python Programming

## Project Overview
This project analyzes global biodiversity data from GBIF to uncover trends in species distribution, taxonomy, and temporal dynamics. It features a premium Streamlit dashboard and a comprehensive LaTeX report.

## Project Structure
- `src/`: Source code for data cleaning, EDA, and the dashboard.
  - `data_cleaning.py`: Script to clean the raw dataset.
  - `eda.py`: Script to generate static figures for the report.
  - `app/`: Contains the Streamlit dashboard application.
- `notebooks/`: Jupyter notebooks.
  - `eda.ipynb`: Interactive exploratory data analysis.
- `reports/`: Project documentation.
  - `report.tex`: LaTeX source for the final report.
  - `figures/`: Generated plots used in the report.
- `data/`: Contains the dataset (ensure `cleaned_dataset.csv` is present).

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run src/app/main.py
```

### 3. Run the Notebook
Open `notebooks/eda.ipynb` in Jupyter or VS Code and execute the cells.
