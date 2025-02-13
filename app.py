import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# 📌 Streamlit App Config
st.set_page_config(page_title="Stock Market Predictor", layout="wide")

# 📌 Title & Search Bar
st.title("📊 Stock Market Prediction Dashboard")
st.subheader("Get AI-powered stock predictions!")

stock_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL").upper()

# 📌 Fetch Stock Data
@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")

data = get_stock_data(stock_symbol)

if not data.empty:
    # 📌 Interactive Chart
    st.subheader(f"Stock Price Trend for {stock_symbol}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
    fig.update_layout(title=f"{stock_symbol} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)")
    st.plotly_chart(fig)

    # 📌 Train Simple Linear Model for Prediction
    st.subheader("📈 AI Stock Prediction")
    data["Days"] = np.arange(len(data)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(data["Days"].values.reshape(-1, 1), data["Close"])

    future_days = np.array([len(data) + i for i in range(1, 6)]).reshape(-1, 1)
    future_prices = model.predict(future_days)

    # 📌 Show Predictions
    prediction_df = pd.DataFrame({"Days Ahead": [1, 2, 3, 4, 5], "Predicted Price": future_prices})
    st.dataframe(prediction_df)

    # 📌 AI Buy/Hold/Sell Recommendation
    if future_prices[-1] > data["Close"].iloc[-1]:
        st.success(f"✅ AI Recommendation: **BUY** {stock_symbol}")
    else:
        st.warning(f"⚠️ AI Recommendation: **HOLD/SELL** {stock_symbol}")

else:
    st.error("⚠️ Invalid Stock Ticker. Try Again.")

# 📌 News Section (Placeholder for API)
st.subheader("📰 Latest Market News")
st.write("📢 News API integration coming soon!")

