import yfinance as yf
import streamlit as st
import pandas as pd
from firebase_admin import firestore
import os
import requests

def get_stock_data(tickers, start_date, end_date):
    """
    Download historical close prices for a list of tickers.
    
    Parameters:
        tickers (list): List of stock symbols (e.g., ['AAPL', 'MSFT'])
        start_date (str): Start date in format 'YYYY-MM-DD'
        end_date (str): End date in format 'YYYY-MM-DD'
    
    Returns:
        pd.DataFrame: DataFrame containing close prices
    """
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    
    return data.dropna()

# def load_tickers():
#     if os.path.exists(ticker_file := "data/tickers_file.csv"):
#         # Load tickers from CSV file
#         return pd.read_csv(ticker_file)["tickers"].to_list()
#     else:
#         return pd.DataFrame(columns=["ticker"])

def get_tickers_from_firestore():
    db = firestore.client()
    docs = db.collection("tickers_db").document("stocks").collection("tickers").stream()
    return [doc.to_dict()["ticker"] for doc in docs]

# Base URL of your Flask API
# API_URL = "http://localhost:5000/tickers"

# # Function to add a new ticker to the API
# def add_ticker_to_api(ticker):
#     response = requests.post(API_URL, json={"ticker": ticker})
#     if response.status_code == 201:
#         st.success("Ticker added successfully!")
#     elif response.status_code == 409:
#         st.warning("Ticker already exists.")
#     else:
#         st.error("Failed to add ticker.")

# # Function to fetch tickers from the API
# def fetch_tickers_from_api():
#     try:
#         response = requests.get(API_URL)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error("Failed to fetch tickers.")
#             return []
#     except Exception as e:
#         st.error(f"API error: {e}")
#         return []

# # Fetch all tickers from the database
# def get_tickers():
#     url = "http://localhost:5000/tickers"
#     response = requests.get(url)
#     return response.json()



def get_latest_price(ticker):
    """
    Fetch the latest stock price for a single ticker.
    
    Parameters:
        ticker (str): Stock symbol (e.g., 'AAPL')
    
    Returns:
        float: Latest price
    """
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d')
    return todays_data['Close'].iloc[-1] if not todays_data.empty else None
