# Stock Market Prediction Dashboard

This project is a simple AI-powered stock market prediction dashboard. It uses **TensorFlow**, **LSTMs**, and **Yahoo Finance API** to fetch stock data, train a model, and predict future stock prices. The dashboard is built using **Streamlit** for easy visualization.

## 🚀 Features
- Fetches historical stock data using **Yahoo Finance API**.
- Trains a **Long Short-Term Memory (LSTM)** neural network to predict stock prices.
- Provides a simple **dashboard** to predict and display stock prices.

---

## 📌 Installation
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/stock-prediction.git
cd stock-prediction
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv # Optionally you can specify a name instead of venv
source venv/bin/activate  # On Windows: tensorflow_env\Scripts\activate

```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
**OR** install manually:
```bash
pip install tensorflow pandas numpy scikit-learn matplotlib seaborn yfinance streamlit
```

### **4. Verify TensorFlow Installation**
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

## 📊 Fetch Stock Market Data
Run the following command to download stock data (Example: Apple - `AAPL`):
```bash
python fetch_data.py
```

---

## 🛠 Preprocess Data
Normalize stock prices for training:
```bash
python preprocess.py
```

---

## 🎯 Train the Model
Train the **LSTM model** using historical stock data:
```bash
python train.py
```
✅ The model will be saved as `stock_model.h5`.

---

## 🔮 Predict Stock Price
Make a prediction for a specific stock ticker (e.g., `AAPL`):
```bash
python predict.py
```
✅ The output will show the predicted stock price for the next day.

---

## 📊 Run the Dashboard
Start the **Streamlit-based** dashboard:
```bash
streamlit run app.py
```
🔗 **Open in your browser:** `http://localhost:8501`

---

## 📤 Deployment (Optional)
Deploy the app on **Render or AWS**:
1. Push the code to **GitHub**.
2. Create a **Render** account.
3. Deploy as a Python web service.

👉 [Render Deployment Guide](https://render.com/docs/deploy-a-python-service)

---

## 📝 Summary
✅ **Set up the environment**  
✅ **Fetched stock data**  
✅ **Trained an LSTM model**  
✅ **Built a simple prediction dashboard**  

🎉 **Now you have a working AI-powered stock prediction dashboard!**

