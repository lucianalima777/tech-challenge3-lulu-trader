# Tech Challenge 3 - Previsão de Preço do Ouro com ML

Este repositório apresenta a solução do **Desafio Técnico da Fase 3 da Pós em Machine Learning Engineering da FIAP**.
Baseado em um desafio familiar bem humorado, decidi juntar meu aprendizado na pós com minha vontade de prever, com meu modelo personalizado e com boa acurácia, o preço do ouro em dólares.
Aqui, combinei técnicas de coleta de dados, modelagem preditiva e visualização para responder a seguinte pergunta:

> **"O preço do ouro vai subir ou cair?"**

---

## Visão Geral

Este projeto foi dividido em **módulos**, cada um com seu papel no fluxo de desenvolvimento:

- `cron/` - Scripts agendados para **coleta diária dos preços do ouro** via API publica (Yahoo Finance);
- `data/` - Diretório que armazena os dados:
  - `raw/`: Dados brutos coletados;
  - `processed/`: Dados transformados e prontos para uso;
  - `gold_prices.db`: Banco de dados SQLite com histórico completo.
- `src/` - Contém a **pipeline de Machine Learning**, responsável pela predição, processamento de features e avaliação.
  - `database/`: Módulo de conexao com SQLite.
- `models/` - Modelo treinado (lulu_model.pkl) salvo em formato pickle.
- `app/` - Código da API FastAPI e interface Streamlit para visualização do sinal gerado.
- `notebooks/` - Análises exploratórias e testes avulsos.
- `README.md` - Onde esta documentado nosso projeto.

---

## Tecnologias Utilizadas

- **Python 3.11**
- **Pandas**, **NumPy** e **Scikit-learn**
- **yfinance** para coleta de dados financeiros
- **SQLite** para armazenamento dos dados
- **FastAPI** para API REST com endpoints
- **Streamlit** para dashboard
- **joblib** para salvar o modelo
- **schedule** para agendamento
- **Git** + **GitHub**

---

## Como Executar Localmente

### 1. Clone o projeto
```bash
git clone 
cd tech-challenge3-ml
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # No caso de Linux/Mac
.venv\Scripts\activate   # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a coleta de dados
```bash
python cron/app.py
```
Isso vai coletar os dados do Yahoo Finance e salvar tanto em CSV quanto no banco SQLite.
> **Obs.:** Pode ocorrer erro de rate limit do Yahoo Finance. Neste caso, utilize os dados já existentes.

### 5. Gere as features processadas
```bash
python src/processing/generate_latest_features.py
```

### 6. Rode a API (opcional)
```bash
uvicorn app.api:app --reload
```

### 7. Inicie o Dashboard
```bash
streamlit run app/streamlit_app.py
```

---

## Como o modelo funciona?

### Coleta e Armazenamento
- A API coleta os **últimos 365 dias** de preço do ouro (ticker GC=F - futuros) via Yahoo Finance.
- Os dados são armazenados em banco SQLite (`data/gold_prices.db`) e também mantidos em CSV para compatibilidade.

### Features
Criei **11 features técnicas** baseadas em indicadores financeiros:
-  `pct_change` - Variação percentual do preço de fechamento
-  `sma_3` - Média móvel simples de 3 dias
- `sma_7` - Média móvel simples de 7 dias
- `std_3` - Desvio padrão móvel de 3 dias (volatilidade)
- `momentum` - Diferença entre preços consecutivos
- `cross_sma` - Indicador de cruzamento de médias móveis
- `amplitude` - Diferença entre máxima e mínima do dia
- `candle_alta` - Flag indicando se o fechamento foi acima da abertura
- `close_2_days_ago` - Preço de fechamento de 2 dias atrás
- `rolling_std_7` - Desvio padrão móvel de 7 dias
**Target:** Binário (1 = preço vai subir, 0 = preço não vai subir)

### Modelo
Trata-se de modelo com previsão conservadora.

### Algoritmo
**Random Forest Classifier**
- 100 estimadores
- Balanceamento de classes com oversample
- Treinamento com divisão temporal (train/test split)

### Performance
- **Acurácia:** 72%
- **Precision (classe alta):** 76%
- **Recall (classe alta):** 59%

### Sistema de Sinais
O modelo retorna probabilidades que são convertidas em 3 recomendações:
- **BUY:** Probabilidade > 60% (alta confiança de subida)
- **HOLD:** Probabilidade entre 40-60% (incerteza)
- **SELL:** Probabilidade < 40% (alta confiança de queda)

---

## Resultado: Dashboard Interativo

O **Streamlit dashboard** mostra:

- Gráfico histórico de preços do último ano
- Preço atual do ativo
- **Probabilidades lado a lado:** Chance de alta vs queda
- **Sinal de trading** com cores intuitivas (verde=BUY, azul=HOLD, vermelho=SELL)
- Acurácia do modelo (73%) para transparência

Ideal para **tomada de decisão visual e rápida**.

---

## API Endpoints

A API FastAPI disponibiliza:

- `GET /` - Status da API
- `GET /coletar-dados` - Coleta novos dados do Yahoo Finance e salva no banco
- `GET /prever-sinal` - Retorna a previsao atual (BUY/HOLD/SELL)

Acesse a documentacao interativa em `http://localhost:8000/docs` apos iniciar a API.

---

## Dashboard

O dashboard Streamlit apresenta:

- Gráfico de série temporal do preço do ouro (último ano)
- Preço atual, máxima e mínima do dia
- Botão para gerar previsão
- Probabilidades de alta vs queda
- Sinal de trading com indicação visual colorida
- Informações sobre acurácia do modelo

---

## Análise Exploratória

Principais descobertas (detalhes no notebook `01_exploracao_dados_ouro.ipynb`):

- 253 observações diárias (out/2024 - out/2025)
- Preço médio: $3.073
- Volatilidade: Alta (desvio padrão de $345)
- Distribuição do target: 58% alta, 42% não alta (desbalanceado)
- Correlações mais fortes: indicadores de curto prazo (SMA 3 dias, preço de 2 dias atrás)
- Outliers detectados mas mantidos (eventos reais de mercado)

---

## Autoria

Este projeto foi desenvolvido por **Luciana Lima** para atender ao Tech Challenge 3 da Pós Graduação em Machine Learning Engineering da FIAP.

---
