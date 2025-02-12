import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(df):
    df = df[['Date', 'Close']]  # Focus on closing prices
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    df['Close'] = scaler.fit_transform(df[['Close']])

    return df, scaler

if __name__ == "__main__":
    from fetch_data import fetch_stock_data
    df, scaler = preprocess_data(fetch_stock_data("AAPL"))
    print(df.head())
