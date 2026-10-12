import pandas as pd
import streamlit as st

# Configuração da página (deve ser sempre a primeira instrução do Streamlit)
st.set_page_config(
    page_title="Arbitragem de Criptomoedas",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Análise de Arbitragem de Criptomoedas")
st.write(
    "Esta aplicação analisa os dados de microstructure e os spreads entre"
    " diferentes corretoras."
)


# Função para carregar os dados e já aplicar os nomes amigáveis
@st.cache_data
def carregar_dados():
  caminho_ficheiro = "data/cross_exchange_spread.csv"
  try:
    df = pd.read_csv(caminho_ficheiro)

    # Dicionário de renomeação para português
    colunas_renomeadas = {
        "date": "Data / Hora",
        "symbol": "Par / Cripto",
        "exchange": "Corretora",
        "regime": "Regime de Mercado",
        "price": "Preço ($)",
        "spread_to_ref_bps": "Spread de Referência (bps)",
        "max_cross_spread_bps": "Spread Máximo Arbitrável (bps)",
        "is_stress": "Estresse de Mercado?",
        "shock_event": "Evento de Choque",
    }
    df = df.rename(columns=colunas_renomeadas)
    return df
  except FileNotFoundError:
    return None


# Carregar o dataset
df = carregar_dados()

if df is not None:
  st.success("Dataset carregado com sucesso!")

  # Mostrar uma prévia dos dados brutos (agora com o st.dataframe incluído!)
  with st.expander("🔍 Ver amostra dos dados brutos"):
    st.dataframe(df.head(10))

  # Métricas / KPIs rápidos no topo
  st.subheader("📊 Indicadores Principais")
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric(label="Total de Registos", value=f"{len(df):,}".replace(",", "."))

  with col2:
    st.metric(label="Total de Colunas", value=len(df.columns))

  with col3:
    st.metric(label="Estado dos Dados", value="Pronto para Análise")

  # Pré-visualização das colunas disponíveis
  st.subheader("🛠️ Explorador de Colunas")
  colunas = df.columns.tolist()
  coluna_selecionada = st.selectbox(
      "Selecione uma coluna para visualizar o gráfico de linhas:", colunas
  )

  if coluna_selecionada:
    # Gráfico simples com base na coluna selecionada (apenas para colunas numéricas)
    try:
      st.line_chart(df[coluna_selecionada].head(200))
    except Exception:
      st.info(
          "ℹ️ Seleciona uma coluna numérica (como Preço ou Spreads) para gerar o"
          " gráfico."
      )

else:
  st.error(
      "⚠️ O ficheiro `cross_exchange_spread.csv` não foi encontrado na pasta"
      " `data/`."
  )
  st.info(
      "Certifica-te de que a pasta se chama `data` e o ficheiro está lá dentro"
      " com exatamente esse nome."
  )