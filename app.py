# Streamlit app
import streamlit as st
st.title('Real-Time Stock Market Data')
symbol = st.text_input('Enter Stock Symbol', 'AAPL')

if symbol:
    stock_data = fetch_stock_data(symbol)
    if stock_data is not None:
        st.write(f'Showing data for {symbol}')
        st.write(stock_data.tail())
        plot_stock_data(stock_data)
    else:
        st.write('Error fetching data. Please check the stock symbol and try again.')
