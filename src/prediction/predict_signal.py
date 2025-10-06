import pandas as pd
import joblib
import os
os.makedirs("models", exist_ok=True)

# Carrega o modelo salvo
model_path = "models/lulu_model.pkl"
modelo = joblib.load(model_path)

# Lista de features na ordem usada no treino
features = [
    "pct_change", "sma_3", "sma_7", "std_3", "momentum",
    "cross_sma", "prev_up", "amplitude", "candle_alta",
    "close_2_days_ago", "rolling_std_7"
]

def predict_signal(input_data: pd.DataFrame, return_proba: bool = False):
    """
    Recebe um DataFrame com as features mais recentes e retorna 'buy', 'hold' ou 'sell'.
    Se return_proba=True, retorna tupla (sinal, probabilidade).
    """
    if not all(feat in input_data.columns for feat in features):
        raise ValueError("Colunas de features ausentes no input!")

    X = input_data[features]
    probas = modelo.predict_proba(X)[:, 1][0]

    if probas > 0.6:
        sinal = "buy"
    elif probas > 0.4:
        sinal = "hold"
    else:
        sinal = "sell"

    if return_proba:
        return sinal, probas
    return sinal


if __name__ == "__main__":
    # Exemplo: carregar CSV com últimas features
    df = pd.read_csv("data/processed/latest_features.csv")
    sinal = predict_signal(df)
    print(f"Sinal de hoje: {sinal.upper()}")
