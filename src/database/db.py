import sqlite3
import pandas as pd

DB_PATH = "data/gold_prices.db"

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dados(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('gold_prices', conn, if_exists='append', index=False)
    conn.close()

def ler_dados():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM gold_prices ORDER BY date DESC', conn)
    conn.close()
    return df
