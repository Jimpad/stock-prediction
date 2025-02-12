import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from preprocess import preprocess_data
from fetch_data import fetch_stock_data

# Load Model
model = load_model("stock_model.h5")

def predict_stock_price(ticker):
    df, scaler = preprocess_data(fetch_stock_data(ticker))
    last_60_days = df['Close'].values[-60:].reshape(1, 60, 1)

    predicted_price = model.predict(last_60_days)
    predicted_price = scaler.inverse_transform(predicted_price)
    
    return predicted_price[0][0]

if __name__ == "__main__":
    price = predict_stock_price("AAPL")
    print(f"Predicted Price: ${price:.2f}")
