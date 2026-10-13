# Corporate Financial & Transaction Analytics Dashboard 📊

An end-to-end Data Science project focusing on financial data extraction, key indicator computation, and interactive business intelligence visualization.

## 🎯 Project Overview
This repository contains a comprehensive analysis of corporate financial conditions and transaction volumes. It transitions from raw data extraction and preprocessing in Jupyter Notebooks to a fully interactive web application built with Streamlit.

## 🏗️ Architecture & Workflow
The project is divided into analytical phases and deployment:
1. **Data Preparation & Cleaning (`notebooks/01`):** Extraction and sanitization of raw financial data.
2. **Financial Metrics (`notebooks/02`):** Computation of core business indicators (Net Profit Margin, Return on Assets/Equity, PEG Ratio, Free Cashflow).
3. **Market Comparison (`notebooks/03`):** Benchmarking target companies against industry peers via `yfinance` API integration and Matplotlib/Seaborn visualizations.
4. **Interactive BI Dashboard (`app.py`):** A Streamlit application utilizing Plotly for dynamic time-series and geographic transaction analysis.

## 🛠️ Tech Stack
* **Languages:** Python
* **Data Processing:** Pandas, NumPy
* **Financial API:** yfinance
* **Visualization:** Plotly, Matplotlib, Seaborn
* **Deployment:** Streamlit

## 🚀 How to Run Locally
1. Clone the repository: `git clone https://github.com/YourUsername/Corporate-Financial-Analytics.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the dashboard: `streamlit run app.py`
