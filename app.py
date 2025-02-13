import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go # type: ignore
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import timedelta

# Page Configuration
st.set_page_config(page_title="Stock Market Predictor", layout="wide")

# Title
st.title("Stock Market Prediction Dashboard")

# Sidebar - Stock Ticker Selection
st.sidebar.header("📈 Stock Selection")
stock_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL").upper()


# Sidebar with Custom Timeframe
st.sidebar.header("⏳ Custom Timeframe Selection")

default_time_options = {
    "1 Hour": ("1d", "5m"),
    "1 Day": ("5d", "15m"),
    "1 Week": ("7d", "1d"),
    "1 Month": ("1mo", "1d"),
    "1 Year": ("1y", "1wk")
}

selected_timeframe = st.sidebar.selectbox("📅 Choose a Timeframe", list(default_time_options.keys()) + ["Custom"])

custom_period, custom_interval = None, None

if selected_timeframe == "Custom":
    tooltip_period = """
        <div style="display: flex; align-items: left;">
            <span>Period</span>
            <span style="cursor: help; color: red; margin-left: 10px;" title="Defines how much historical stock data to retrieve.">?</span>
        </div>
    """
    tooltip_interval = """
        <div style="display: flex; align-items: left;">
            <span>Interval</span>
            <span style="cursor: help; color: red; margin-left: 5px;" title="Determines the frequency of data points (e.g., daily, weekly).">?</span>
        </div>
    """

    st.sidebar.markdown(tooltip_period, unsafe_allow_html=True)
    custom_period = st.sidebar.text_input("Period (e.g., 1d, 5d, 1mo, 1y, max)", "1mo")

    st.sidebar.markdown(tooltip_interval, unsafe_allow_html=True)
    custom_interval = st.sidebar.text_input("Interval (e.g., 1d, 1wk)", "1d")

# Validation for custom period and interval
valid_periods = ["1d", "5d", "1mo", "1y", "max"]
valid_intervals = ["1d", "1wk"]

if selected_timeframe == "Custom":
    # Period validation
    if custom_period not in valid_periods:
        st.error("❌ Invalid Period! Please use one of the following: 1d, 5d, 1mo, 1y, max.")
        custom_period = None  # Reset if invalid

    # Interval validation
    if custom_interval not in valid_intervals:
        st.error("❌ Invalid Interval! Please use one of the following: 1d, 1wk.")
        custom_interval = None  # Reset if invalid

period, interval = default_time_options[selected_timeframe] if selected_timeframe != "Custom" else (custom_period, custom_interval)

@st.cache_data
def get_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    return stock.history(period=period, interval=interval)

if period and interval:
    data = get_stock_data(stock_symbol, period, interval)

    # Floating Price Box under the Timeframe Selector
    if not data.empty:
        last_close = data["Close"].iloc[-1]
        prev_close = data["Close"].iloc[-2] if len(data) > 1 else last_close
        change = last_close - prev_close
        change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
        arrow = "↑" if change > 0 else "↓"
        color = "green" if change > 0 else "red"

        st.sidebar.markdown(f"""
            <div style="background-color: transparent; padding: 10px; border-radius: 10px; text-align: center;">
                <span style="color: {color}; font-size: 18px; font-weight: bold;">{arrow} {stock_symbol}</span><br>
                <span style="font-size: 22px; color: white;">${last_close:.2f}</span><br>
                <span style="color: {color};">{change:.2f} ({change_pct:.2f}%)</span>
            </div>
        """, unsafe_allow_html=True)

        # Stock Price Chart
        st.subheader(f"📊 {stock_symbol} Price Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price"))
        fig.update_layout(title=f"{stock_symbol} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig)

        # AI Stock Prediction
        st.subheader("📈 AI Stock Prediction")

        # Adding Days and Dates for Prediction
        data["Days"] = np.arange(len(data)).reshape(-1, 1)
        model = LinearRegression()
        model.fit(data["Days"].values.reshape(-1, 1), data["Close"])

        # Predict for the next 5 days
        future_days = np.array([len(data) + i for i in range(1, 6)]).reshape(-1, 1)
        future_prices = model.predict(future_days)

        # Create a new DataFrame with more detailed prediction information
        prediction_dates = pd.date_range(start=data.index[-1] + timedelta(days=1), periods=5, freq='D')
        
        prediction_df = pd.DataFrame({
            "Prediction Date": prediction_dates,
            "Days Ahead": [1, 2, 3, 4, 5],
            "Predicted Price (USD)": future_prices,
            "Price Change (USD)": future_prices - data["Close"].iloc[-1],
            "Price Change (%)": (future_prices - data["Close"].iloc[-1]) / data["Close"].iloc[-1] * 100
        })

        # Calculate additional metrics
        prediction_df["Upper Bound (USD)"] = future_prices + (future_prices * 0.05)  # Example: 5% above prediction
        prediction_df["Lower Bound (USD)"] = future_prices - (future_prices * 0.05)  # Example: 5% below prediction

        # Simple Volatility Estimate (using historical data) - Could be improved with more sophisticated methods
        historical_volatility = data["Close"].pct_change().std() * np.sqrt(252) # Annualized Volatility
        prediction_df["Volatility (%)"] = historical_volatility * 100 # Add volatility to the prediction table


        # AI Buy/Hold/Sell Recommendation (Improved)
        last_close = data["Close"].iloc[-1]
        predicted_change_pct = (future_prices[-1] - last_close) / last_close * 100

        if predicted_change_pct > 5:  # Example threshold: 5% increase
            st.success(f"✅ AI Recommendation: **Strong BUY** {stock_symbol} (Projected {predicted_change_pct:.2f}% increase)")
        elif predicted_change_pct > 2: # Example threshold: 2% increase
            st.info(f"✅ AI Recommendation: **BUY** {stock_symbol} (Projected {predicted_change_pct:.2f}% increase)")
        elif predicted_change_pct < -5:  # Example threshold: 5% decrease
            st.error(f"⚠️ AI Recommendation: **Strong SELL** {stock_symbol} (Projected {predicted_change_pct:.2f}% decrease)")
        elif predicted_change_pct < -2: # Example threshold: 2% decrease
            st.warning(f"⚠️ AI Recommendation: **SELL** {stock_symbol} (Projected {predicted_change_pct:.2f}% decrease)")
        else:
            st.warning(f"⚠️ AI Recommendation: **HOLD** {stock_symbol} (Projected {predicted_change_pct:.2f}% change)")


        # Display the prediction DataFrame
        st.dataframe(prediction_df, use_container_width=True)

        
else:
    st.error("⚠️ Invalid Stock Ticker. Try Again.")

# News Section (Placeholder for API)
st.subheader("📰 Latest Market News")
st.write("📢 News API integration coming soon!")
