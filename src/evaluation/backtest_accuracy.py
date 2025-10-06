import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report

# Carregar dados com as features
df = pd.read_csv("data/raw/gold_price.csv")

# Carregar modelo treinado
modelo = joblib.load("models/lulu_model.pkl")

# Lista de features usadas no treino
features = [
    "pct_change", "sma_3", "sma_7", "std_3", "momentum",
    "cross_sma", "prev_up", "amplitude", "candle_alta",
    "close_2_days_ago", "rolling_std_7"
]

# Garantir que não há NaNs
df.dropna(inplace=True)

# Separar X e y
X = df[features]
y = df["target"]

# Fazer predições
probas = modelo.predict_proba(X)[:, 1]
y_pred = (probas > 0.5).astype(int)

# Mostrar resultados
print("Acurácia:", accuracy_score(y, y_pred))
print(classification_report(y, y_pred))