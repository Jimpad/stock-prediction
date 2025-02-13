import re
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go # type: ignore

# Page Configuration
st.set_page_config(page_title="Finance Dashboard", layout="wide")

# ---- Sidebar (Drawer) ----
with st.sidebar:
    st.header("📌 Stock Finder & AI Recommender")

    # Search Bar
    stock_symbol = st.text_input("Search Stocks:", "AAPL", placeholder="Enter stock ticker (e.g., AAPL, TSLA)")

    # AI Stock Recommendation System
    st.subheader("🤖 AI Stock Recommendations")
    st.markdown("🔍 Our AI suggests stocks based on market trends and momentum.")

    # Dummy AI Recommendations
    ai_recommendations = ["TSLA", "NVDA", "AMD", "GOOGL", "MSFT"]
    st.write(f"✨ **Top Picks:** {', '.join(ai_recommendations)}")

    # ---- Timeframe Selection ----
    st.subheader("⏳ Timeframe Selection")

    time_options = {
        "1H": ("1d", "5m"),
        "1D": ("1d", "15m"),
        "1W": ("7d", "1h"),
        "1M": ("1mo", "1d"),
        "6M": ("6mo", "1d"),
        "1Y": ("1y", "1d"),
        "Max": ("max", "1mo"),
        "Custom": None,
    }

    selected_time = st.selectbox("Select Timeframe:", list(time_options.keys()))

    # Custom timeframe fields
    valid_periods = {"d", "mo", "y", "h", "m"}
    valid_intervals = {
        "1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
    }

    period, interval = None, None
    if selected_time == "Custom":
        period_input = st.text_input("Enter Period (e.g., 5d, 1mo, 1y, max):", "1mo")
        interval_input = st.text_input("Enter Interval (e.g., 1m, 5m, 1h, 1d):", "1d")

        # Validate Period
        period_match = re.match(r"^(\d+)([a-zA-Z]+)$", period_input)
        if period_match and period_match.group(2) in valid_periods:
            period = period_input
        else:
            st.error("❌ Invalid period format! Example of correct usage: `5d`, `1mo`, `1y`, `max`")

        # Validate Interval
        if interval_input in valid_intervals:
            interval = interval_input
        else:
            st.error("❌ Invalid interval format! Example of correct usage: `1m`, `5m`, `1h`, `1d`, `1wk`, `1mo`")

    else:
        period, interval = time_options[selected_time]

# ---- Stock Data Chart ----
st.subheader(f"📊 {stock_symbol} Stock Analysis")
data = yf.Ticker(stock_symbol).history(period=period, interval=interval)
if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price", line=dict(color="blue")))
    st.plotly_chart(fig, use_container_width=True)



# ---- Market Overview (Dynamic Index Fetching) ----
st.subheader("🌎 Market Overview")
col1, col2, col3, col4, col5 = st.columns(5)

index_tickers = {
    "DAX": "^GDAXI",
    "FTSE 100": "^FTSE",
    "CAC 40": "^FCHI",
    "IBEX 35": "^IBEX",
    "STOXX 50": "^STOXX50E"
}

@st.cache_data
def get_market_indexes(index_dict, period, interval):  # Add interval as an argument
    market_data = {}
    for name, ticker in index_dict.items():
        try:
            stock = yf.Ticker(ticker)

            # Determine the appropriate period for intraday data
            if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "1h"]: # Include 1h
                intraday_period = "60d"  # Or "90d" if you need more intraday history. Free tier has limitations.
            else:
                intraday_period = period  # Use the selected period for daily or longer intervals

            hist = stock.history(period=intraday_period, interval=interval)  # Use intraday period if necessary

            if not hist.empty:
                last_close = hist["Close"].iloc[-1]
                prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else last_close
                change = last_close - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                market_data[name] = (last_close, change_pct, change)
        except Exception as e:
            print(f"Error fetching data for {name} ({ticker}): {e}")
            continue
    return market_data


# Display Market Index Data (Updated)
def display_market_data(period, interval):  # Add interval as an argument
    market_indexes = get_market_indexes(index_tickers, period, interval)  # Pass period AND interval
    cols = st.columns(len(market_indexes))

    for col, (index, (value, change_pct, change_abs)) in zip(cols, market_indexes.items()):
        color = "green" if "+" in str(change_pct) else "red"
        col.markdown(f"""
            <div style="border-radius: 10px; padding: 10px; text-align:center; background-color: #1c1c1c;">
                <b>{index}</b><br>
                <span style="font-size: 18px;">{value:.2f}</span><br>
                <span style="color: {color}; font-size: 14px;">{change_pct:+.2f}% ({change_abs:+.2f})</span>
            </div>
        """, unsafe_allow_html=True)

# Call the display function initially and whenever the timeframe changes
display_market_data(period, interval)  # Initial display with default period

# Add a callback to update the market data when the selected_time changes
def update_market_data():
    st.experimental_rerun()  # Rerun the script to update the market data

st.session_state.time_changed = False  # Initialize a session state variable

if st.session_state.time_changed:  # Check if the time has changed
    display_market_data(period, interval)  # Update market data display
    st.session_state.time_changed = False  # Reset the flag

# Add an onChange callback to the selectbox
st.session_state.selected_time = selected_time # Store selected time in session state

if st.session_state.selected_time != selected_time: # Check if selected time has changed
    st.session_state.time_changed = True  # Set the flag if the time has changed
    update_market_data() # Call the function to trigger the update
    st.session_state.selected_time = selected_time # Update selected time in session state



# Styling with CSS for DataFrame (Updated)
st.markdown("""
<style>
    .top-stocks-container {
        width: 100%;
        display: flex;
        flex-wrap: wrap; /* Allow wrapping */
        justify-content: space-around; /* Distribute space */
        gap: 2%;
    }
    .top-movers-container, .top-losers-container {
        background-color: #1e1e1e;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 10px;
        width: 100%; /* Adjust as needed */
        display: inline-block;
        vertical-align: top;
        box-sizing: border-box; /* Include padding and border in width */
    }
    .top-movers-container h3, .top-losers-container h3 {
        text-align: left;
    }
    .top-mover, .top-loser {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 30px;
        padding: 10px 15px;
        border-bottom: 1px solid #444;
        font-size: 16px;
        height: 40px; /* Fixed height for vertical alignment */
    }
    .ticker {
        text-align: left;
    }
    .price {
        text-align: center;
        flex-grow: 1; /* Allow price to take up available space */
        justify-content: center; /* Center horizontally within price cell */
    }
    .change {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Fetch Top Movers & Losers (Restored List-Based Approach)
tickers = ["AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "META", "NFLX", "AMD", "AMZN", "BA", "F", "INTC"]

@st.cache_data
def get_stock_data(ticker_list, period, interval):  # Add period and interval arguments
    stock_data = []
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            
            # Determine the appropriate period for intraday data
            if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "1h"]: # Include 1h
                intraday_period = "60d"  # Or "90d" if you need more intraday history. Free tier has limitations.
            else:
                intraday_period = period  # Use the selected period for daily or longer intervals

            hist = stock.history(period=intraday_period, interval=interval)  # Use intraday period if necessary


            if not hist.empty:
                last_close = hist["Close"].iloc[-1]
                prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else last_close
                change = last_close - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                stock_data.append((ticker, last_close, change, change_pct))
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue
    return stock_data


def display_top_movers_losers(period, interval): # Function to display movers/losers

    stocks = get_stock_data(tickers, period, interval) # Pass period and interval
    df = pd.DataFrame(stocks, columns=["Ticker", "Price", "Change", "Change %"])
    if not df.empty:
        df_sorted = df.sort_values(by="Change %", ascending=False)
        top_movers_list = df_sorted.head(5).values.tolist()
        top_losers_list = df_sorted.tail(5).values.tolist()

        # Dynamically generate signal_strengths from top movers
        signal_strengths = {}
        for ticker, _, _, change_pct in top_movers_list:
            if change_pct > 0:
                signal_strengths[ticker] = "Strong Buy"
            elif change_pct < 0:
                signal_strengths[ticker] = "Sell"
            else:
                signal_strengths[ticker] = "Hold"

        # --- Sidebar ---
        with st.sidebar:  # Keep sidebar code within the display function

            # Strong Buy/Hold/Sell System (Updated)
            st.subheader("📊 Investment Signals")
            st.write(f"📌 **{stock_symbol} Signal:** {signal_strengths.get(stock_symbol, 'No Data')}")


            st.markdown('<div class="top-stocks-container">', unsafe_allow_html=True)

        # Top Movers
        st.markdown('<div class="top-movers-container"><h3 style="color: green;">🚀 Top Movers</h3>', unsafe_allow_html=True)
        for ticker, price, change, change_pct in top_movers_list:  # Iterate through the list
            st.markdown(f"<div class='top-mover'><span class='ticker'><b>{ticker}</b></span><span class='price'>${price:.2f}</span><span class='change'>+{change:.2f} (+{change_pct:.2f}%)</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Top Losers
        st.markdown('<div class="top-losers-container"><h3 style="color: red;">🔻 Top Losers</h3>', unsafe_allow_html=True)
        for ticker, price, change, change_pct in top_losers_list:  # Iterate through the list
            st.markdown(f"<div class='top-mover'><span class='ticker'><b>{ticker}</b></span><span class='price'>${price:.2f}</span><span class='change'>-{abs(change):.2f} ({change_pct:.2f}%)</span></div>", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    else:
        st.warning("Could not retrieve data for the selected tickers.")



display_top_movers_losers(period, interval) # Pass both period and interval

