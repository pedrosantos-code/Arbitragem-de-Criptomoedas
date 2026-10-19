from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Arbitragem de Criptomoedas",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }
    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7ebf2;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 2px 8px rgba(22, 34, 51, 0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #5b6575;
    }
    @media (max-width: 640px) {
        .block-container {
            padding: 1.25rem 1rem 2rem;
        }
        h1 {
            font-size: 1.7rem !important;
        }
        [data-testid="stMetric"] {
            padding: 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados():
    caminho_ficheiro = Path(__file__).resolve().parent / "data" / "cross_exchange_spread.csv"
    df = pd.read_csv(caminho_ficheiro)

    colunas_renomeadas = {
        "date": "Data / Hora",
        "symbol": "Par / Cripto",
        "exchange": "Corretora",
        "regime": "Regime de Mercado",
        "price": "Preço ($)",
        "spread_to_ref_bps": "Spread de Referência (bps)",
        "max_cross_spread_bps": "Spread Máximo (bps)",
        "is_stress": "Estresse de Mercado?",
        "shock_event": "Evento de Choque",
    }
    df = df.rename(columns=colunas_renomeadas)
    df["Data / Hora"] = pd.to_datetime(df["Data / Hora"], errors="coerce")

    for coluna in ("Preço ($)", "Spread de Referência (bps)", "Spread Máximo (bps)"):
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df["Estresse de Mercado?"] = (
        pd.to_numeric(df["Estresse de Mercado?"], errors="coerce")
        .fillna(0)
        .astype(bool)
    )
    return df.dropna(subset=["Data / Hora", "Spread Máximo (bps)"])


try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Não foi possível encontrar `data/cross_exchange_spread.csv`.")
    st.info("Confirme se o arquivo está na pasta `data/` do projeto.")
    st.stop()

st.title("📈 Radar de spreads")
st.caption(
    "Explore diferenças históricas de preços entre corretoras. "
    "Os spreads são brutos e não incluem taxas, slippage ou custos de saque."
)

st.sidebar.header("🎛️ Filtros")

corretoras_disponiveis = sorted(df["Corretora"].dropna().unique().tolist())
corretoras_selecionadas = st.sidebar.multiselect(
    "Corretoras",
    options=corretoras_disponiveis,
    default=corretoras_disponiveis,
)

pares_disponiveis = sorted(df["Par / Cripto"].dropna().unique().tolist())
pares_selecionados = st.sidebar.multiselect(
    "Pares",
    options=pares_disponiveis,
    default=pares_disponiveis,
)

regimes_disponiveis = sorted(df["Regime de Mercado"].dropna().unique().tolist())
regimes_selecionados = st.sidebar.multiselect(
    "Regimes de mercado",
    options=regimes_disponiveis,
    default=regimes_disponiveis,
)

data_minima = df["Data / Hora"].min().date()
data_maxima = df["Data / Hora"].max().date()
periodo = st.sidebar.date_input(
    "Período",
    value=(data_minima, data_maxima),
    min_value=data_minima,
    max_value=data_maxima,
    format="DD/MM/YYYY",
)

if len(periodo) == 2:
    inicio, fim = periodo
else:
    inicio = fim = periodo[0]

df_filtrado = df[
    df["Corretora"].isin(corretoras_selecionadas)
    & df["Par / Cripto"].isin(pares_selecionados)
    & df["Regime de Mercado"].isin(regimes_selecionados)
    & df["Data / Hora"].dt.date.between(inicio, fim)
]

st.caption(
    f"Período analisado: {inicio:%d/%m/%Y} – {fim:%d/%m/%Y} · "
    f"{len(df_filtrado):,} registros".replace(",", ".")
)

st.subheader("Resumo do período")
col1, col2, col3, col4 = st.columns(4)

if df_filtrado.empty:
    with col1:
        st.metric("Maior spread bruto", "—")
    with col2:
        st.metric("Spread médio", "—")
    with col3:
        st.metric("Registros", "0")
    with col4:
        st.metric("Eventos de estresse", "0")
    st.info("Nenhum dado encontrado para os filtros selecionados.")
else:
    eventos_estresse = df_filtrado.loc[
        df_filtrado["Estresse de Mercado?"],
        ["Data / Hora", "Par / Cripto"],
    ].drop_duplicates()

    with col1:
        st.metric(
            "Maior spread bruto",
            f"{df_filtrado['Spread Máximo (bps)'].max():.2f} bps",
        )
    with col2:
        st.metric(
            "Spread médio",
            f"{df_filtrado['Spread Máximo (bps)'].mean():.2f} bps",
        )
    with col3:
        st.metric("Registros", f"{len(df_filtrado):,}".replace(",", "."))
    with col4:
        st.metric("Eventos de estresse", f"{len(eventos_estresse):,}".replace(",", "."))

    st.subheader("Evolução dos spreads")
    serie_temporal = (
        df_filtrado.groupby(["Data / Hora", "Par / Cripto"], as_index=False)
        ["Spread Máximo (bps)"]
        .max()
    )
    media_periodo = serie_temporal["Spread Máximo (bps)"].mean()
    fig = px.line(
        serie_temporal,
        x="Data / Hora",
        y="Spread Máximo (bps)",
        color="Par / Cripto",
        labels={
            "Data / Hora": "Data",
            "Spread Máximo (bps)": "Spread bruto (bps)",
            "Par / Cripto": "Ativo",
        },
        color_discrete_sequence=["#2563eb", "#14b8a6"],
    )
    fig.add_hline(
        y=media_periodo,
        line_dash="dot",
        line_color="#94a3b8",
        annotation_text="Média do período",
        annotation_position="top left",
    )
    fig.update_layout(
        template="plotly_white",
        height=390,
        margin=dict(l=8, r=8, t=24, b=8),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(
        fig,
        width="stretch",
        config={"responsive": True, "displaylogo": False},
    )

    st.subheader("Maiores spreads observados")
    melhores_spreads = (
        df_filtrado.sort_values("Spread Máximo (bps)", ascending=False)
        .drop_duplicates(subset=["Data / Hora", "Par / Cripto"])
        .loc[
            :,
            [
                "Data / Hora",
                "Par / Cripto",
                "Spread Máximo (bps)",
                "Regime de Mercado",
                "Estresse de Mercado?",
            ],
        ]
        .head(10)
        .rename(
            columns={
                "Data / Hora": "Data",
                "Spread Máximo (bps)": "Spread bruto (bps)",
                "Regime de Mercado": "Regime",
                "Estresse de Mercado?": "Estresse",
            }
        )
    )
    melhores_spreads["Data"] = melhores_spreads["Data"].dt.strftime("%d/%m/%Y")
    st.dataframe(
        melhores_spreads,
        hide_index=True,
        width="stretch",
        column_config={
            "Spread bruto (bps)": st.column_config.NumberColumn(format="%.2f"),
            "Estresse": st.column_config.CheckboxColumn(),
        },
    )

with st.expander("Sobre os dados e a metodologia"):
    st.write(
        "A base contém observações históricas por ativo e corretora. "
        "O spread máximo é repetido entre corretoras para a mesma data e ativo; "
        "por isso, o gráfico e a lista de destaques consolidam essas repetições. "
        "Um spread positivo não garante uma oportunidade executável ou lucrativa "
        "após taxas, slippage, liquidez e latência."
    )
