import numpy as np
import tensorflow as tf
from model import create_lstm_model
from preprocess import preprocess_data
from fetch_data import fetch_stock_data

# Load and preprocess data
df, scaler = preprocess_data(fetch_stock_data("AAPL"))

# Prepare sequences
def create_sequences(data, seq_length=60):
    sequences, labels = [], []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
        labels.append(data[i + seq_length])
    return np.array(sequences), np.array(labels)

data = df['Close'].values.reshape(-1, 1)
X, y = create_sequences(data)

X = np.reshape(X, (X.shape[0], X.shape[1], 1))  # Reshape for LSTM

# Train Model
model = create_lstm_model((X.shape[1], 1))
model.fit(X, y, batch_size=16, epochs=10)

# Save Model
model.save("stock_model.h5")
