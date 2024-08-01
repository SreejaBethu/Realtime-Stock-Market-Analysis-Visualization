import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

# Set up Streamlit app
st.set_page_config(layout="wide")
st.title('Real-Time Stock Market Data')

# Input for stock ticker
stock_ticker = st.text_input('Enter stock ticker:', 'AAPL').upper()


# Fetching data
def fetch_data():
    try:
        apple_stock = yf.Ticker(stock_ticker)
        historical_prices = apple_stock.history(period='1d', interval='1m')
        return historical_prices
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None


# Plotting today's data
def plot_data(df_today):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_today, x=df_today.index, y='Close', ax=ax)
    ax.set_title(f"{stock_ticker} Intraday Price", fontsize=16)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Closing Price (USD)", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)


# Main logic
if st.button('Fetch Data') or True:
    df = fetch_data()

    if df is not None:
        # Display available timestamps
        st.write("Available timestamps:")
        st.write(df.index)

        # Filter for today's data
        today = datetime.now().date()  # Use local date
        df_today = df[df.index.date == today]

        if not df_today.empty:
            st.subheader(f"Today's data for {stock_ticker}")
            plot_data(df_today)
        else:
            st.warning(f"No intraday data available for {stock_ticker} today.")
    else:
        st.error(f"No data available for the ticker {stock_ticker}.")

# Optional: Add a refresh button to fetch the latest data
if st.button('Refresh Data'):
    st.experimental_set_query_params(refresh=str(datetime.now()))

# Infinite Loop to Fetch and Update Stock Values
while True:
    df = fetch_data()

    if df is not None:
        # Display available timestamps
        st.write("Available timestamps:")
        st.write(df.index)

        # Filter for today's data
        today = datetime.now().date()  # Use local date
        df_today = df[df.index.date == today]

        if not df_today.empty:
            st.subheader(f"Today's data for {stock_ticker}")
            plot_data(df_today)
        else:
            st.warning(f"No intraday data available for {stock_ticker} today.")

        # Show the latest stock value in the app
        latest_price = df_today['Close'].iloc[-1]
        latest_time = df_today.index[-1].strftime('%H:%M:%S')
        st.write(f"Latest Price ({latest_time}): {latest_price}")

        # Sleep for 60 sec before fetching new data
        time.sleep(60)