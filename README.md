
# International Debt Analysis System

## Project Overview

This project provides an end-to-end analysis of international external debt using the World Bank International Debt Statistics (IDS) dataset.

The project covers data cleaning, exploratory data analysis (EDA), database management, SQL analysis, and interactive dashboard development using Python, PostgreSQL, Streamlit, and Power BI.

**Analysis Period:** 2000–2024

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- PostgreSQL
- SQL
- Streamlit
- Power BI
- Jupyter Notebook

## Project Workflow

1. Data collection from World Bank International Debt Statistics
2. Data cleaning and preprocessing using Python
3. Exploratory Data Analysis (EDA)
4. PostgreSQL database creation and data import
5. SQL queries for debt analysis
6. Interactive dashboard development using Streamlit
7. Power BI dashboard development
8. Final project documentation

## Key Analysis

- Global external debt trends from 2000 to 2024
- Top 10 countries by external debt
- Country-wise debt comparisons
- Regional debt analysis
- Year-over-year debt growth
- Country debt rankings
- Debt contribution percentages
- Indicator-wise debt analysis

## Project Files

| File | Description |
|------|-------------|
| `home.ipynb` | Python data cleaning and EDA |
| `app.py` | Streamlit analytics application |
| `International_dept_22092026.sql` | PostgreSQL SQL analysis |
| `requirements.txt` | Python dependencies |
| `IDS_CountryMetaData_cleaned.csv` | Cleaned country metadata |
| `IDS_FootNoteMetaData_cleaned.csv` | Cleaned footnote metadata |
| `IDS_SeriesMetaData_cleaned.csv` | Cleaned indicator metadata |
| `International_Debt_Analysis_Final_Report.pdf` | Final project report |
| `International_Debt_Analysis_Final_Report.docx` | Editable project report |

## Download Power BI Dashboard and Dataset

The Power BI dashboard and complete cleaned dataset are available in GitHub Releases.

**[Download Project Files - Release v1.0.0](https://github.com/chitrashree059-tech/International-Debt-Analysis/releases/tag/v1.0.0)**

Release assets:

- `International_Debt_Analysis_Dashboard.pbix`
- `IDS_ALLCountries_Data_cleaned.csv`

## How to Run the Streamlit Application

### 1. Clone the repository

```bash
git clone https://github.com/chitrashree059-tech/International-Debt-Analysis.git
cd International-Debt-Analysis
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Install PostgreSQL and create a database named `international_debt`.

Create and populate the required tables using the project's SQL scripts and cleaned data.

Configure the database connection in `app.py` for your local PostgreSQL setup.

Set the `DB_PASSWORD` environment variable to your PostgreSQL password.

### 4. Run Streamlit

```bash
streamlit run app.py
```

## Data Source

World Bank - International Debt Statistics (IDS)

https://databank.worldbank.org/source/international-debt-statistics

## Project Documentation

The repository includes a final project report covering the methodology, data preprocessing, exploratory analysis, SQL analysis, dashboards, and project findings.

## Project Status

Completed - End-to-end Data Analytics Project

## Author

Chitra R

Data Analytics and Data Science Learner
