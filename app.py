import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página (deve ser sempre a primeira instrução do Streamlit)
st.set_page_config(
    page_title="Arbitragem de Criptomoedas",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Análise de Arbitragem de Criptomoedas")
st.write(
    "Esta aplicação analisa dados de microstructure e os spreads entre"
    " diferentes corretoras de forma interativa."
)


# Função para carregar os dados e já aplicar os nomes amigáveis em português
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

  # --- BARRA LATERAL (Filtros Dinâmicos) ---
  st.sidebar.header("🎛️ Filtros do Dashboard")

  # Filtro por Corretora
  corretoras_disponiveis = df["Corretora"].unique().tolist()
  corretora_selecionada = st.sidebar.multiselect(
      "Selecione a Corretora:",
      options=corretoras_disponiveis,
      default=corretoras_disponiveis,
  )

  # Filtro por Par / Cripto
  pares_disponiveis = df["Par / Cripto"].unique().tolist()
  par_selecionado = st.sidebar.multiselect(
      "Selecione o Par / Cripto:",
      options=pares_disponiveis,
      default=pares_disponiveis,
  )

  # Aplicar os filtros ao DataFrame principal
  df_filtrado = df[
      df["Corretora"].isin(corretora_selecionada)
      & df["Par / Cripto"].isin(par_selecionado)
  ]

  # --- MÉTRICAS / KPIS PRINCIPAIS ---
  st.subheader("📊 Indicadores Principais")
  col1, col2, col3 = st.columns(3)

  with col1:
    st.metric(
        label="Registos Filtrados",
        value=f"{len(df_filtrado):,}".replace(",", "."),
    )

  with col2:
    st.metric(label="Corretoras Selecionadas", value=len(corretora_selecionada))

  with col3:
    st.metric(label="Pares Selecionados", value=len(par_selecionado))

  # --- GRÁFICO INTERATIVO COM PLOTLY ---
  st.subheader("📊 Evolução Gráfica do Spread Máximo")

  if not df_filtrado.empty:
    # Criar um gráfico Plotly interativo para as primeiras 500 linhas filtradas
    fig = px.line(
        df_filtrado.head(500),
        x="Data / Hora",
        y="Spread Máximo Arbitrável (bps)",
        color="Corretora",
        title="Spread Máximo por Corretora ao Longo do Tempo",
        markers=True,
    )
    fig.update_layout(
        xaxis_title="Data / Hora",
        yaxis_title="Spread Máximo Arbitrável (bps)",
        legend_title="Corretora",
    )
    st.plotly_chart(fig, use_container_width=True)
  else:
    st.warning(
        "⚠️ Não existem dados disponíveis para os filtros selecionados na barra"
        " lateral."
    )

  # --- PRÉ-VISUALIZAÇÃO DOS DADOS BRUTOS ---
  with st.expander("🔍 Ver amostra dos dados filtrados"):
    st.dataframe(df_filtrado.head(20), use_container_width=True)

else:
  st.error(
      "⚠️ O ficheiro `cross_exchange_spread.csv` não foi encontrado na pasta"
      " `data/`."
  )
  st.info(
      "Certifica-te de que a pasta se chama `data` e o ficheiro está lá dentro"
      " com exatamente esse nome."
  )