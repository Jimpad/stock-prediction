import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="5y", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df

if __name__ == "__main__":
    df = fetch_stock_data("AAPL")  # Example: Apple stock
    print(df.head())
