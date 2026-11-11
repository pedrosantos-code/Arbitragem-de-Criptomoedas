import html
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
    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .stApp {
        --canvas: light-dark(#f3f6f8, #080b12);
        --border: light-dark(rgba(55, 75, 96, 0.16), rgba(148, 163, 184, 0.14));
        --muted: light-dark(#5f6f82, #91a0b5);
        --text: light-dark(#172435, #e8eef7);
        --mint: light-dark(#087f69, #65f0c2);
        background:
            radial-gradient(ellipse at 10% 0%, light-dark(rgba(8, 127, 105, 0.12), rgba(35, 91, 107, 0.18)), transparent 34rem),
            radial-gradient(ellipse at 92% 8%, light-dark(rgba(91, 93, 180, 0.09), rgba(67, 56, 142, 0.16)), transparent 30rem),
            var(--canvas);
        color: var(--text);
    }
    .print-filter-summary {
        display: none;
    }
    [data-testid="stHeader"] {
        background: light-dark(rgba(243, 246, 248, 0.82), rgba(8, 11, 18, 0.72));
        backdrop-filter: blur(14px);
    }
    [data-testid="stMainMenuItem-theme-System"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            light-dark(#edf2f5, #0d1420) 0%,
            light-dark(#f5f7f9, #0a1019) 100%
        );
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: var(--text);
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: light-dark(#e8f5f1, #18382f) !important;
        border: 1px solid light-dark(rgba(8, 127, 105, 0.22), rgba(101, 240, 194, 0.32));
        border-radius: 999px !important;
        color: light-dark(#086c59, #b7f7e1) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: light-dark(#086c59, #b7f7e1) !important;
        fill: currentColor;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelectTagsContainer"] [data-tag] {
        background-color: light-dark(#e8f5f1, #18382f) !important;
        border: 1px solid light-dark(rgba(8, 127, 105, 0.22), rgba(101, 240, 194, 0.32)) !important;
        border-radius: 999px !important;
        color: light-dark(#086c59, #b7f7e1) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelectTagsContainer"] [data-tag] button {
        background: transparent !important;
        color: inherit !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [role="group"]:has(> [data-testid="stMultiSelectTagsContainer"]),
    [data-testid="stSidebar"] [data-testid="stDateInputField"],
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div {
        background: light-dark(#e8f5f1, #101a26) !important;
        border-color: light-dark(rgba(8, 127, 105, 0.22), rgba(101, 240, 194, 0.32)) !important;
        border-radius: 10px !important;
    }
    .block-container {
        max-width: 1520px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    .hero-card {
        position: relative;
        overflow: hidden;
        padding: 2rem 2.15rem;
        margin-bottom: 1.6rem;
        border: 1px solid light-dark(rgba(55, 75, 96, 0.16), rgba(148, 163, 184, 0.17));
        border-radius: 22px;
        background:
            radial-gradient(ellipse at 83% 18%, light-dark(rgba(8, 127, 105, 0.12), rgba(101, 240, 194, 0.15)), transparent 24rem),
            linear-gradient(
                112deg,
                light-dark(rgba(255, 255, 255, 0.98), rgba(18, 29, 42, 0.98)),
                light-dark(rgba(243, 247, 249, 0.96), rgba(13, 19, 31, 0.94)) 56%,
                light-dark(rgba(238, 241, 249, 0.96), rgba(20, 25, 43, 0.94))
            );
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.22);
    }
    .hero-card:after {
        content: "";
        position: absolute;
        top: 0;
        right: 12%;
        width: 1px;
        height: 100%;
        background: linear-gradient(transparent, light-dark(rgba(8, 127, 105, 0.24), rgba(101, 240, 194, 0.28)), transparent);
        transform: rotate(28deg);
    }
    .hero-kicker, .section-kicker {
        color: var(--mint);
        font-size: 0.7rem;
        font-weight: 750;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }
    .hero-title {
        margin: 0.65rem 0 0.45rem;
        color: light-dark(#142132, #f5f8fc);
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 720;
        letter-spacing: -0.055em;
        line-height: 1.08;
    }
    .hero-copy {
        max-width: 680px;
        margin: 0;
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.65;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1.2rem;
        padding: 0.45rem 0.72rem;
        border: 1px solid light-dark(rgba(8, 127, 105, 0.22), rgba(101, 240, 194, 0.22));
        border-radius: 999px;
        background: light-dark(rgba(8, 127, 105, 0.07), rgba(101, 240, 194, 0.07));
        color: light-dark(#086c59, #b7f7e1);
        font-size: 0.72rem;
        font-weight: 650;
        letter-spacing: 0.04em;
    }
    .hero-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--mint);
        box-shadow: 0 0 12px light-dark(rgba(8, 127, 105, 0.48), rgba(101, 240, 194, 0.8));
    }
    .section-heading {
        margin: 1.4rem 0 0.2rem;
        color: light-dark(#172435, #f2f6fb);
        font-size: 1.16rem;
        font-weight: 680;
        letter-spacing: -0.025em;
    }
    [data-testid="stMetric"] {
        min-height: 122px;
        background: linear-gradient(
            145deg,
            light-dark(rgba(255, 255, 255, 0.98), rgba(21, 31, 46, 0.96)),
            light-dark(rgba(238, 243, 247, 0.96), rgba(13, 20, 31, 0.92))
        );
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.05rem 1.15rem;
        box-shadow: 0 10px 28px light-dark(rgba(29, 47, 66, 0.08), rgba(0, 0, 0, 0.12));
        transition: border-color 160ms ease, transform 160ms ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: light-dark(rgba(8, 127, 105, 0.34), rgba(101, 240, 194, 0.34));
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.82rem;
    }
    [data-testid="stMetricValue"] {
        color: light-dark(#172435, #f2f7fb);
        font-size: 1.5rem;
        font-weight: 680;
    }
    [data-testid="stDataFrame"] {
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-color: light-dark(#c6d0dc, #29374a);
        border-radius: 10px;
    }
    input,
    textarea {
        color-scheme: inherit;
    }
    [data-testid="stCaption"], .stMarkdown p {
        color: var(--muted);
    }
    [data-testid="stExpander"] {
        border-color: var(--border);
        border-radius: 14px;
        background: light-dark(rgba(255, 255, 255, 0.72), rgba(16, 23, 35, 0.55));
    }
    .js-plotly-plot text {
        fill: light-dark(#536273, #a9b7c8) !important;
    }
    .js-plotly-plot .gridlayer path {
        stroke: light-dark(rgba(91, 107, 125, 0.2), rgba(148, 163, 184, 0.12)) !important;
    }
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    @page {
        size: A4 portrait;
        margin: 14mm;
    }
    @media print {
        html,
        body {
            height: auto !important;
            min-height: 0 !important;
            color-scheme: light !important;
            background: #ffffff !important;
            color: #172435 !important;
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
        }
        .stApp {
            --canvas: #ffffff;
            --border: #d7dee7;
            --muted: #526174;
            --text: #172435;
            --mint: #087f69;
            height: auto !important;
            min-height: 0 !important;
            color-scheme: light !important;
            background: #ffffff !important;
            color: #172435 !important;
        }
        [data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="stToolbar"],
        [data-testid="stStatusWidget"],
        [data-testid="stElementToolbar"],
        [data-testid="stMainMenu"] {
            display: none !important;
        }
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stScreencast"] {
            height: auto !important;
            max-height: none !important;
            min-height: 0 !important;
            overflow: visible !important;
            background: #ffffff !important;
            color: #172435 !important;
        }
        .block-container {
            width: 100% !important;
            max-width: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .hero-card,
        [data-testid="stMetric"],
        [data-testid="stExpander"] {
            break-inside: avoid;
            page-break-inside: avoid;
            background: #ffffff !important;
            border-color: #d7dee7 !important;
            box-shadow: none !important;
            color: #172435 !important;
        }
        .hero-card:after {
            display: none;
        }
        .hero-title,
        .section-heading,
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"],
        .hero-copy,
        .hero-kicker,
        .section-kicker,
        .hero-badge,
        [data-testid="stCaption"],
        .stMarkdown p {
            color: #172435 !important;
        }
        .hero-kicker,
        .section-kicker {
            color: #087f69 !important;
        }
        .hero-badge {
            background: #eef8f5 !important;
            border-color: #b7ddd2 !important;
        }
        .print-filter-summary {
            display: block !important;
            margin: 0 0 1rem;
            padding: 0.65rem 0.8rem;
            border: 1px solid #d7dee7;
            border-radius: 8px;
            color: #172435 !important;
            font-size: 0.8rem;
            line-height: 1.5;
        }
        [data-testid="stMetric"] {
            min-height: 0 !important;
            padding: 0.75rem !important;
        }
        [data-testid="stPlotlyChart"],
        [data-testid="stDataFrame"],
        .js-plotly-plot {
            break-inside: avoid;
            page-break-inside: avoid;
            max-width: 100% !important;
            box-shadow: none !important;
        }
        [data-testid="stColumn"]:has(.js-plotly-plot) {
            flex: 1 1 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }
        .js-plotly-plot text {
            fill: #334155 !important;
        }
        .js-plotly-plot .gridlayer path {
            stroke: #d7dee7 !important;
        }
        .js-plotly-plot .barlayer path {
            fill: #087f69 !important;
        }
        .js-plotly-plot .modebar-container {
            display: none !important;
        }
    }
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.85rem 2.25rem;
        }
        .hero-card {
            padding: 1.45rem 1.25rem;
            border-radius: 17px;
        }
        .hero-title {
            font-size: 2rem;
        }
        [data-testid="stMetric"] {
            min-height: 108px;
            padding: 0.8rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.15rem;
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

st.markdown(
    """
    <section class="hero-card">
      <div class="hero-kicker">Market intelligence · cripto</div>
      <h1 class="hero-title">Radar de spreads</h1>
      <p class="hero-copy">
        Compare diferenças históricas de preços entre corretoras e entenda
        como os spreads mudam conforme o ativo e o regime de mercado.
      </p>
      <span class="hero-badge"><span class="hero-dot"></span> ANÁLISE HISTÓRICA · SEM DADOS EM TEMPO REAL</span>
    </section>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## Filtros")
st.sidebar.caption("Ajuste o recorte para explorar o histórico.")

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

comparacao_valida = len(corretoras_selecionadas) >= 2
if comparacao_valida:
    spreads_por_ativo = (
        df_filtrado.groupby(["Data / Hora", "Par / Cripto"], as_index=False)
        .agg(
            spread_minimo=("Spread de Referência (bps)", "min"),
            spread_maximo=("Spread de Referência (bps)", "max"),
            **{
                "Regime de Mercado": ("Regime de Mercado", "first"),
                "Estresse de Mercado?": ("Estresse de Mercado?", "max"),
            },
        )
    )
    spreads_por_ativo["Spread Máximo (bps)"] = (
        spreads_por_ativo["spread_maximo"] - spreads_por_ativo["spread_minimo"]
    )
else:
    spreads_por_ativo = pd.DataFrame()

st.markdown(
    '<div class="section-kicker">Visão geral</div>'
    '<div class="section-heading">Resumo do período</div>',
    unsafe_allow_html=True,
)
st.caption(
    f"{inicio:%d/%m/%Y} — {fim:%d/%m/%Y} · "
    f"{len(corretoras_selecionadas)} corretoras · "
    f"{len(df_filtrado):,} observações".replace(",", ".")
)
filtros_impressao = (
    f"<strong>Corretoras:</strong> {html.escape(', '.join(corretoras_selecionadas) or 'Nenhuma')} &nbsp;·&nbsp; "
    f"<strong>Pares:</strong> {html.escape(', '.join(pares_selecionados) or 'Nenhum')} &nbsp;·&nbsp; "
    f"<strong>Regimes:</strong> {html.escape(', '.join(regimes_selecionados) or 'Nenhum')} &nbsp;·&nbsp; "
    f"<strong>Período:</strong> {inicio:%d/%m/%Y} — {fim:%d/%m/%Y}"
)
st.markdown(
    f'<div class="print-filter-summary">{filtros_impressao}</div>',
    unsafe_allow_html=True,
)
col1, col2, col3, col4 = st.columns(4)
eventos_estresse = df_filtrado.loc[
    df_filtrado["Estresse de Mercado?"],
    ["Data / Hora", "Par / Cripto"],
].drop_duplicates()

if spreads_por_ativo.empty:
    with col1:
        st.metric("Maior spread bruto", "—", help="Exige ao menos duas corretoras.")
    with col2:
        st.metric("Spread médio", "—")
    with col3:
        st.metric("Registros", f"{len(df_filtrado):,}".replace(",", "."))
    with col4:
        st.metric("Eventos de estresse", f"{len(eventos_estresse):,}".replace(",", "."))
    if not comparacao_valida:
        st.info("Selecione pelo menos duas corretoras para calcular spreads comparáveis.")
    else:
        st.info("Nenhum dado encontrado para os filtros selecionados.")
else:
    with col1:
        st.metric(
            "Maior spread bruto",
            f"{spreads_por_ativo['Spread Máximo (bps)'].max():.2f} bps",
        )
    with col2:
        st.metric(
            "Spread médio",
            f"{spreads_por_ativo['Spread Máximo (bps)'].mean():.2f} bps",
        )
    with col3:
        st.metric("Registros", f"{len(df_filtrado):,}".replace(",", "."))
    with col4:
        st.metric("Eventos de estresse", f"{len(eventos_estresse):,}".replace(",", "."))

    st.markdown(
        '<div class="section-kicker">Série temporal</div>'
        '<div class="section-heading">Como o spread evoluiu</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Diferença entre as referências das corretoras selecionadas, por ativo. "
        "A linha pontilhada mostra a média do recorte."
    )
    serie_temporal = spreads_por_ativo[
        [
            "Data / Hora",
            "Par / Cripto",
            "Regime de Mercado",
            "Spread Máximo (bps)",
        ]
    ]
    media_periodo = serie_temporal["Spread Máximo (bps)"].mean()
    grafico_col, ativos_col = st.columns([1.8, 1], gap="large")
    with grafico_col:
        fig = px.line(
            serie_temporal,
            x="Data / Hora",
            y="Spread Máximo (bps)",
            color="Par / Cripto",
            line_dash="Regime de Mercado",
            hover_data=["Regime de Mercado"],
            labels={
                "Data / Hora": "Data",
                "Spread Máximo (bps)": "Spread bruto (bps)",
                "Par / Cripto": "Ativo",
                "Regime de Mercado": "Regime",
            },
            color_discrete_sequence=["#65f0c2", "#8b9bff", "#ffba75"],
        )
        fig.add_hline(
            y=media_periodo,
            line_dash="dot",
            line_color="#9aa9bd",
            annotation_text="Média",
            annotation_position="top left",
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#a9b7c8", size=11),
            height=420,
            margin=dict(l=8, r=8, t=32, b=8),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=False, zeroline=False, title=None),
            yaxis=dict(gridcolor="rgba(148,163,184,0.12)", zeroline=False, title=None),
        )
        st.plotly_chart(
            fig,
            width="stretch",
            config={"responsive": True, "displaylogo": False},
        )

    with ativos_col:
        st.markdown(
            '<div class="section-kicker">Comparativo</div>'
            '<div class="section-heading">Pico por ativo</div>',
            unsafe_allow_html=True,
        )
        st.caption("Maior spread observado no período, em bps.")
        picos_por_ativo = (
            spreads_por_ativo.groupby("Par / Cripto", as_index=False)
            .agg(pico=("Spread Máximo (bps)", "max"))
            .sort_values("pico", ascending=True)
        )
        fig_ativos = px.bar(
            picos_por_ativo,
            x="pico",
            y="Par / Cripto",
            orientation="h",
            text="pico",
            labels={"pico": "Pico do spread (bps)", "Par / Cripto": "Ativo"},
            color="pico",
            color_continuous_scale=["#41506c", "#65f0c2"],
        )
        fig_ativos.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            cliponaxis=False,
            marker_line_width=0,
        )
        fig_ativos.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#a9b7c8", size=11),
            height=290,
            margin=dict(l=8, r=38, t=32, b=8),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)", title=None),
            yaxis=dict(showgrid=False, title=None),
        )
        st.plotly_chart(
            fig_ativos,
            width="stretch",
            config={"responsive": True, "displaylogo": False},
        )

    st.markdown(
        '<div class="section-kicker">Destaques históricos</div>'
        '<div class="section-heading">Maiores spreads observados</div>',
        unsafe_allow_html=True,
    )
    st.caption("Os maiores valores do recorte selecionado; não representam lucro líquido.")
    melhores_spreads = (
        spreads_por_ativo.sort_values("Spread Máximo (bps)", ascending=False)
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
        "O spread é recalculado para cada data e ativo usando apenas as corretoras "
        "selecionadas: a diferença entre o maior e o menor spread em relação à "
        "referência. Assim, adicionar ou remover corretoras atualiza os indicadores, "
        "o gráfico e a lista de destaques. O regime de mercado aparece na legenda "
        "e ao passar o cursor sobre o gráfico. "
        "Um spread positivo não garante uma oportunidade executável ou lucrativa "
        "após taxas, slippage, liquidez e latência."
    )
