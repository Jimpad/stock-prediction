import streamlit as st
from predict import predict_stock_price

st.title("📈 Stock Market Prediction Dashboard")
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)")

if ticker:
    predicted_price = predict_stock_price(ticker)
    st.success(f"Predicted Price for {ticker}: ${predicted_price:.2f}")
