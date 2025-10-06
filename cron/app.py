import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.database.db import criar_tabela, salvar_dados

def baixar_preco_ouro():
    criar_tabela()

    ouro = yf.Ticker("GC=F")
    df = ouro.history(period="1y", interval="1d")

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Salvar no SQLite
    df_db = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df_db.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    salvar_dados(df_db)

    # Manter CSV tambem
    script_dir = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(script_dir, "..", "data", "raw", "gold_price.csv")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)

    print(f"[{datetime.now()}] Dados salvos em CSV e banco SQLite")

if __name__ == "__main__":
    baixar_preco_ouro()
