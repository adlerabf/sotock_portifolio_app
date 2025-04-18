# 📊 Stock Portfolio Analyzer

A Streamlit-based application for analyzing and forecasting stock portfolios using historical data, financial metrics, and machine learning models.

---

## 🚀 Project Overview

This application allows users to:
- Select and manage a portfolio of stocks
- Visualize historical performance and key metrics
- Calculate return, volatility, Sharpe ratio, and correlation
- Forecast future performance using models like Prophet or LSTM
- Compare performance with market benchmarks (IBOV, S&P500)
- Run Monte Carlo simulations and perform backtesting
- Export results and receive automated risk alerts

---

## 🧠 Technologies Used

| Category         | Tools & Libraries                      |
|------------------|----------------------------------------|
| Web Interface    | Streamlit                              |
| Data Source      | Yahoo Finance API (via `yfinance`)     |
| Data Analysis    | Pandas, NumPy                          |
| Visualization    | Plotly, Matplotlib                     |
| ML & Forecasting | Scikit-learn, Prophet, TensorFlow/Keras|
| Deployment       | Docker, Streamlit Community Cloud      |

---

## 🗂️ Project Structure

stock_portfolio_app/ │ ├── app.py # Main Streamlit app ├── requirements.txt # Project dependencies ├── Dockerfile # Container configuration │ ├── data/ # Raw and processed data ├── models/ # Trained forecasting models ├── notebooks/ # EDA and experiments ├── utils/ # Helper scripts │ ├── data_loader.py # Functions for data collection │ ├── analytics.py # Portfolio metrics and KPIs │ └── forecasting.py # ML forecasting models │ └── README.md # Project documentation


---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/stock_portfolio_app.git
cd stock_portfolio_app
---

### Create and activate a virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

### Install dependencies

pip install -r requirements.txt

### Run the app

streamlit run app.py

