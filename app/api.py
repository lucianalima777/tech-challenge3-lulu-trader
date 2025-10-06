import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import certifi
from fastapi import FastAPI
from src.prediction.predict_signal import predict_signal
from src.database.db import criar_tabela, salvar_dados

os.environ['SSL_CERT_FILE'] = certifi.where()

app = FastAPI()

def baixar_preco_ouro():
    criar_tabela()

    ouro = yf.Ticker("GC=F")
    df = ouro.history(period="1y", interval="1d")

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Salva no SQLite
    df_db = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df_db.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    salvar_dados(df_db)

    # Mantém, alternativamente, os dados no CSV
    os.makedirs("data/raw", exist_ok=True)
    caminho = "data/raw/gold_price.csv"
    df.to_csv(caminho, index=False)

    print(f"[{datetime.now()}] Dados salvos em CSV e banco SQLite")
    return True

@app.get("/")
def status():
    return {"mensagem": "API de coleta de dados do ouro está no ar"}

@app.get("/coletar-dados")
def coletar_dados():
    sucesso = baixar_preco_ouro()
    if sucesso:
        return {"status": "sucesso", "mensagem": "Dados coletados e salvos no banco SQLite"}
    return {"status": "erro", "mensagem": "Falha ao coletar dados"}

@app.get("/prever-sinal")
def prever_sinal():
    df = pd.read_csv("data/processed/latest_features.csv")
    resultado = predict_signal(df)
    return {"sinal": resultado}