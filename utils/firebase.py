import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import yfinance as yf
import json

def initialize_firebase():
    # Load credentials from JSON Streamlit secrets
    cred_json = st.secrets["firebase"]["credentials"]

    # Parse string to dictionary
    cred_dict = json.loads(cred_json)

    # Initialize Firebase app if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

def add_tickers_to_firebase():
    initialize_firebase()
    db = firestore.client()

    st.sidebar.subheader("Add New Tickers")
    tickers_input = st.sidebar.text_input("Enter tickers separated by comma (e.g., AAPL,MSFT,PETR4.SA)", "")

    if st.sidebar.button("Add Tickers"):
        if tickers_input.strip() == "":
            st.sidebar.warning("Please enter at least one ticker.")
        else:
            added = []
            already_exists = []
            invalid = []

            tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

            for ticker in tickers:
                doc_ref = db.collection("tickers_db").document("stocks").collection("tickers").document(ticker)
                doc = doc_ref.get()

                if doc.exists:
                    already_exists.append(ticker)
                    continue

                # Validate with yfinance
                try:
                    ticker_info = yf.Ticker(ticker).info
                    if 'regularMarketPrice' in ticker_info and ticker_info['regularMarketPrice'] is not None:
                        doc_ref.set({"ticker": ticker})
                        added.append(ticker)
                    else:
                        invalid.append(ticker)
                except Exception:
                    invalid.append(ticker)

            # Feedback messages
            if added:
                st.sidebar.success(f"✅ Added: {', '.join(added)}")
            if already_exists:
                st.sidebar.info(f"ℹ️ Already exists: {', '.join(already_exists)}")
            if invalid:
                st.sidebar.error(f"❌ Invalid: {', '.join(invalid)}. Please check the 'How to format tickers guide'.")
