import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.prediction.predict_signal import predict_signal
from src.processing.generate_latest_features import *

st.title("Lulu Trader - Previsão de Ouro")

st.write("Sistema de recomendação de compra ou venda do ouro baseado em Machine Learning - Tech Challenge 3")

# Carrega dados históricos
try:
    df_raw = pd.read_csv("data/raw/gold_price.csv")
    df_raw["Date"] = pd.to_datetime(df_raw["Date"])

    st.subheader("Histórico de Preços (Último Ano)")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_raw["Date"], df_raw["Close"], label="Preço de Fechamento")
    ax.set_xlabel("Data - Mês/Ano")
    ax.set_ylabel("Preço (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Informações do último dia
    st.subheader("Dados Atuais")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Preço de Fechamento", f"${df_raw['Close'].iloc[-1]:.2f}")

    with col2:
        st.metric("Mínima do Dia", f"${df_raw['Low'].iloc[-1]:.2f}")

    with col3:
        st.metric("Máxima do Dia", f"${df_raw['High'].iloc[-1]:.2f}")

    st.caption(f"Última atualização: {df_raw['Date'].iloc[-1].strftime('%d/%m/%Y')}")

except FileNotFoundError:
    st.error("Dados não encontrados. Execute a coleta de dados primeiro.")

# Botão para gerar de previsão/sinal
st.subheader("Previsão de Sinal")

if st.button("Gerar Previsão"):
    try:
        df_features = pd.read_csv("data/processed/latest_features.csv")
        sinal, proba = predict_signal(df_features, return_proba=True)

        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probabilidade de Alta", f"{proba:.1%}")
        with col2:
            st.metric("Probabilidade de Queda", f"{(1-proba):.1%}")
        st.write("---")

        if sinal == "buy":
            st.success(f"SINAL: {sinal.upper()} - Recomendação de compra")
        elif sinal == "hold":
            st.info(f"SINAL: {sinal.upper()} - Manter posição, aguardar")
        else:
            st.error(f"SINAL: {sinal.upper()} - Recomendação de venda")

        st.caption("Modelo treinado com acurácia de 72% no conjunto de dados coletados.")

    except FileNotFoundError:
        st.error("Features não encontradas. Execute o processamento primeiro.")
    except Exception as e:
        st.error(f"Erro ao gerar previsão: {e}")