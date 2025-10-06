import pandas as pd
import joblib

modelo = joblib.load("models/lulu_model.pkl")

features = [
    "pct_change", "sma_3", "sma_7", "std_3", "momentum",
    "cross_sma", "prev_up", "amplitude", "candle_alta",
    "close_2_days_ago", "rolling_std_7"
]

df = pd.read_csv("data/processed/latest_features.csv")
X = df[features]

proba = modelo.predict_proba(X)[:, 1][0]

print(f"Probabilidade de subida: {proba:.2%}")
print(f"Probabilidade de queda: {(1-proba):.2%}")

if proba > 0.6:
    print("Sinal: BUY")
elif proba > 0.4:
    print("Sinal: HOLD")
else:
    print("Sinal: SELL")