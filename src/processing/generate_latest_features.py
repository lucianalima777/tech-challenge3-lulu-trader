import pandas as pd
import os

# Caminho do dataset
path = "data/raw/gold_price.csv"
df = pd.read_csv(path)
df["pct_change"] = df["Close"].pct_change()
df["sma_3"] = df["Close"].rolling(window=3).mean()
df["sma_7"] = df["Close"].rolling(window=7).mean()
df["std_3"] = df["Close"].rolling(window=3).std()
df["momentum"] = df["Close"] - df["Close"].shift(1)
df["cross_sma"] = (df["sma_3"] > df["sma_7"]).fillna(0).astype(int)
df["prev_up"] = (df["Close"].diff() > 0).shift(1).fillna(0).astype(int)
df["amplitude"] = df["High"] - df["Low"]
df["candle_alta"] = (df["Close"] > df["Open"]).fillna(0).astype(int)
df["close_2_days_ago"] = df["Close"].shift(2)
df["rolling_std_7"] = df["Close"].rolling(window=7).std()

# Remove qualquer linha com NaN restante
df.dropna(inplace=True)

# Pega a última linha com todas as features
latest = df[[
    "pct_change", "sma_3", "sma_7", "std_3", "momentum",
    "cross_sma", "prev_up", "amplitude", "candle_alta",
    "close_2_days_ago", "rolling_std_7"
]].tail(1)

# Criação da pasta
os.makedirs("data/processed", exist_ok=True)

# Salva no CSV
latest.to_csv("data/processed/latest_features.csv", index=False)

print("Arquivo 'latest_features.csv' gerado com sucesso!")
