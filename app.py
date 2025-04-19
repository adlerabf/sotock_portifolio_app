# Libs
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore


# Utils
from utils.data_loader import get_stock_data, get_latest_price, get_tickers_from_firestore
from utils.portifolio_analysis import calculate_portfolio_performance
from utils.plots import plot_time_series
from utils.firebase import initialize_firebase, add_tickers_to_firebase

# Init Firebase
initialize_firebase()

st.set_page_config(page_title="Stock Portfolio Analyzer", layout="wide")
st.title("📊 Stock Portfolio Analyzer")


st.sidebar.subheader("📈 Enter your stock tickers")



# Instruções sobre os sufixos
with st.sidebar.expander("📘 How to format tickers"):
    st.markdown("""
    Use Yahoo Finance formatting when entering tickers.  
    Add the correct **suffix** based on the exchange:

    | Country        | Exchange                   | Suffix | Example     |
    |----------------|----------------------------|--------|-------------|
    | USA            | NYSE / NASDAQ              | *(none)* or `.US` | `AAPL`, `MSFT` |
    | Brazil         | B3                         | `.SA`  | `PETR4.SA`  |
    | Canada         | Toronto Stock Exchange     | `.TO`  | `RY.TO`     |
    | UK             | London Stock Exchange      | `.L`   | `HSBA.L`    |
    | Germany        | Frankfurt Stock Exchange   | `.DE`  | `VOW3.DE`   |
    | India          | NSE / BSE                  | `.NS` / `.BO` | `TCS.NS`, `RELIANCE.BO` |
    | China          | Shanghai / Shenzhen        | `.SS` / `.SZ` | `601318.SS`, `000001.SZ` |
    | ...            | ...                        | ...    | ...         |

    👉 If you are not sure about a ticker, search it directly on [Yahoo Finance](https://finance.yahoo.com/).
    """)

# import streamlit as st
# import requests



# def fetch_tickers_from_api():
#     try:
#         response = requests.get("https://sotock-portifolio-app.onrender.com/tickers")
#         if response.status_code == 200:
#             return response.json()
#         else:
#             st.error("Failed to load tickers from API.")
#             return []
#     except Exception as e:
#         st.error(f"Error fetching tickers: {e}")
#         return []

# # Define an initial list of tickers
# initial_tickers = load_tickers()

# # Check if the tickers list already exists in session_state, if not, initialize it
# if "tickers_list" not in st.session_state:
#     st.session_state.tickers_list = initial_tickers

# # Function to add a new ticker to the list
# def add_ticker_to_list(ticker):
#     if ticker and ticker not in st.session_state.tickers_list:
#         st.session_state.tickers_list.append(ticker)

# # Input field for adding new tickers
# st.sidebar.subheader("📈 Add new Ticker")
# new_ticker = st.sidebar.text_input("Enter new ticker (e.g., AAPL)")

# # Button to add the ticker to the list
# if st.sidebar.button("Add Ticker"):
#     add_ticker_to_list(new_ticker)
#     st.sidebar.success(f"✅ Ticker {new_ticker} added!")

# # Display the available tickers (the default ones plus any user-added ones)
# st.sidebar.subheader("📊 Available Tickers")
# st.sidebar.write(st.session_state.tickers_list)

# # tickers = st.session_state.tickers_list

# Firestore client
db = firestore.client()

# Add tikkers to Firestore
add_tickers_to_firebase()


# Processando entrada
#tickers = load_tickers()
tickers = get_tickers_from_firestore()


# Define default date range
end_date = datetime.today()
start_date = end_date - timedelta(days=365)



# Create layout with columns
col1, col2 = st.columns(2)


# Tickers selection
   
    


# Date input
with col2:
    start = st.date_input("Start Date", value=start_date)
    end = st.date_input("End Date", value=end_date)


with col1:
    tickers_selected = st.multiselect(
    "📈 Select Your Assets",
    options=tickers,
    default=None,
    placeholder="Type or select tickers...",
    help="if you didn't found the ticker you are looking for, please add it in the sidebar.", 
    )



# Select tickers to include in portfolio

if tickers_selected:
    with col1:
        st.write("🎯 Portfolio Weights Allocator")
        st.markdown("Adjust the weight of one asset. The others will be automatically scaled to make the total = 1.")
        # Select one ticker to manually assign weight
        fixed_ticker = st.selectbox("Select one asset to assign weight manually:", tickers_selected)
   
        # User sets weight for the fixed ticker
        fixed_weight = st.slider(f"Set weight for {fixed_ticker}", min_value=0.0, max_value=1.0, value=1.0, step=0.01)

        # Calculate weights for remaining tickers
        other_tickers = [ticker for ticker in tickers_selected if ticker != fixed_ticker]
        remaining_weight = round(1.0 - fixed_weight, 6)

        if other_tickers:
            auto_weight = round(remaining_weight / len(other_tickers), 6)
        else:
            auto_weight = 0.0
    with col2:
        # Construct the final weights dictionary
        weights = {ticker: auto_weight for ticker in other_tickers}
        weights[fixed_ticker] = fixed_weight

        # Display results
        st.markdown("#### Final Portfolio Weights")
        st.dataframe(pd.DataFrame.from_dict(weights, orient='index', columns=["Weight"]).sort_values(by="Weight", ascending=False))
    st.success(f"✅ Total weight: {sum(weights.values()):.4f}")
else:
    st.info("Please select at least one ticker in the previous section.")

# Load and display data
if tickers_selected and start and end and sum(weights.values()) == 1.0:
    # Fetch latest prices
    data = get_stock_data(tickers_selected, start, end)
    st.subheader("📈 Historical Prices")
    plot_time_series(data, y=-0.25)
    st.dataframe(data.tail())

    st.subheader("📊 Portifolio Returns")

    

   # Calculate performance
    portfolio_returns, cumulative_returns = calculate_portfolio_performance(data, weights)

    # CARD - Cumulative return as percentage
    final_return_percent = cumulative_returns[-1] * 100

    st.metric(label="📈 Cumulative Return", 
              value=f"{final_return_percent:.2f}%",
              )

    # LINE CHART - Daily return chart
    fig = px.line(x=portfolio_returns.index, y=portfolio_returns * 100,
                labels={'x': 'Date', 'y': 'Daily Return (%)'},
                title="📉 Daily Portfolio Return (%)")
    st.plotly_chart(fig, use_container_width=True)


