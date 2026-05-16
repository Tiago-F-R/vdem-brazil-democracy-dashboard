import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Democracia no Brasil", layout="wide")



COLS = [
    'country_name', 'country_text_id', 'year',
    'v2x_polyarchy', 'v2x_libdem', 'v2x_partipdem',
    'v2x_egaldem', 'v2x_delibdem', 'v2x_liberal',
    'v2xcl_rol', 'v2x_freexp_altinf', 'v2x_frassoc_thick',
    'v2xel_frefair', 'v2x_accountability', 'v2x_corr',
    'v2xcs_ccsi', 'v2x_gender', 'v2x_execorr',
    'v2x_jucon', 'v2xlg_legcon',
]

INDICES = {
    "Democracia Liberal":        "v2x_libdem",
    "Democracia Eleitoral":      "v2x_polyarchy",
    "Democracia Participativa":  "v2x_partipdem",
    "Democracia Igualitária":    "v2x_egaldem",
    "Democracia Deliberativa":   "v2x_delibdem",
    "Liberdade de Expressão":    "v2x_freexp_altinf",
    "Liberdade de Associação":   "v2x_frassoc_thick",
    "Eleições Livres e Justas":  "v2xel_frefair",
    "Estado de Direito":         "v2xcl_rol",
    "Controle da Corrupção":     "v2x_accountability",
    "Restrições ao Executivo":   "v2xlg_legcon",
    "Restrições Judiciais":      "v2x_jucon",
    "Empoderamento Feminino":    "v2x_gender",
    "Sociedade Civil":           "v2xcs_ccsi",
}

LATAM = [
    'Brazil', 'Argentina', 'Chile', 'Colombia', 'Mexico',
    'Peru', 'Uruguay', 'Venezuela', 'Bolivia', 'Ecuador', 'Paraguay',
]
OECD = [
    'United States of America', 'Germany', 'France', 'Sweden', 'Japan',
]
COUNTRY_PT = {
    'Brazil': 'Brasil', 'Argentina': 'Argentina', 'Chile': 'Chile',
    'Colombia': 'Colômbia', 'Mexico': 'México', 'Peru': 'Peru',
    'Uruguay': 'Uruguai', 'Venezuela': 'Venezuela', 'Bolivia': 'Bolívia',
    'Ecuador': 'Equador', 'Paraguay': 'Paraguai',
    'United States of America': 'EUA', 'Germany': 'Alemanha',
    'France': 'França', 'Sweden': 'Suécia', 'Japan': 'Japão',
}

EVENTS = {
    1964: "Golpe militar",
    1985: "Redemocratização",
    1988: "Nova Constituição",
    1995: "FHC I",
    1999: "FHC II",
    2003: "Lula I",
    2007: "Lula II",
    2011: "Dilma I",
    2015: "Dilma II",
    2016: "Impeachment",
    2019: "Bolsonaro I",
    2023: "Lula III",
}

@st.cache_data
def load_data():
    df = pd.read_csv(
        "V-Dem-CY-Full+Others-v16.csv",
        usecols=lambda c: c in COLS,
    )
    return df

with st.spinner("Carregando dados do V-Dem..."):
    df_full = load_data()

brazil  = df_full[df_full["country_name"] == "Brazil"].copy()
df_comp = df_full[df_full["country_name"].isin(LATAM + OECD)].copy()


st.sidebar.header("Controles")

year_range = st.sidebar.slider(
    "Período de análise",
    min_value=int(df_full["year"].min()),
    max_value=int(df_full["year"].max()),
    value=(1945, 2025),
    step=1,
)

selected_indices_labels = st.sidebar.multiselect(
    "Índices - série temporal",
    options=list(INDICES.keys()),
    default=["Democracia Liberal", "Democracia Eleitoral", "Liberdade de Expressão"],
)

show_events = st.sidebar.toggle("Marcar eventos históricos", value=True)

st.sidebar.divider()

comp_countries = st.sidebar.multiselect(
    "Países para comparação",
    options=[c for c in df_comp["country_name"].unique() if c != "Brazil"],
    default=["Argentina", "Chile", "Uruguay", "Venezuela"],
    format_func=lambda x: COUNTRY_PT.get(x, x),
)
comp_index_label = st.sidebar.selectbox(
    "Índice - comparação e mapa",
    options=list(INDICES.keys()),
    index=0,
)
comp_year = st.sidebar.slider(
    "Ano - comparação e mapa",
    min_value=year_range[0],
    max_value=year_range[1],
    value=min(2024, year_range[1]),
)


brazil_filtered = brazil[
    (brazil["year"] >= year_range[0]) & (brazil["year"] <= year_range[1])
]


st.title("Democracia Liberal no Brasil")
st.caption("Fonte: V-Dem Project, versão 16 (2026). Indicadores de 0 a 1.")

latest = brazil[brazil["year"] == brazil["year"].max()].iloc[0]
prev   = brazil[brazil["year"] == brazil["year"].max() - 5].iloc[0]

metric_cols = st.columns(5)
showcase = [
    ("Democracia Liberal",     "v2x_libdem"),
    ("Democracia Eleitoral",   "v2x_polyarchy"),
    ("Liberdade de Expressão", "v2x_freexp_altinf"),
    ("Estado de Direito",      "v2xcl_rol"),
    ("Controle da Corrupção",  "v2x_accountability"),
]
for col, (label, var) in zip(metric_cols, showcase):
    delta = latest[var] - prev[var]
    col.metric(label, f"{latest[var]:.3f}", f"{delta:+.3f} (5 anos)")

st.divider()


st.subheader("Evolução dos índices democráticos no Brasil")

if not selected_indices_labels:
    st.info("Selecione ao menos um índice na barra lateral.")
else:
    selected_vars = [INDICES[l] for l in selected_indices_labels]
    plot_df = brazil_filtered[["year"] + selected_vars].melt(
        id_vars="year", var_name="var", value_name="valor"
    )
    var_to_label = {v: k for k, v in INDICES.items()}
    plot_df["Índice"] = plot_df["var"].map(var_to_label)

    fig_ts = px.line(
        plot_df, x="year", y="valor", color="Índice",
        labels={"year": "Ano", "valor": "Índice (0–1)"},
        height=450,
    )
    fig_ts.update_traces(line_width=2.2)
    fig_ts.update_layout(yaxis_range=[0, 1], legend_title_text="")

    if show_events:
        for yr, label in EVENTS.items():
            if year_range[0] <= yr <= year_range[1]:
                fig_ts.add_vline(
                    x=yr, line_dash="dot", line_color="gray", line_width=1,
                    annotation_text=label, annotation_position="top",
                    annotation_font_size=10, annotation_textangle=-90,
                )

    st.plotly_chart(fig_ts, use_container_width=True)

st.divider()


st.subheader("Mapa mundial")

map_var = INDICES[comp_index_label]

map_df = df_full[df_full["year"] == comp_year][
    ["country_name", "country_text_id", map_var]
].dropna(subset=[map_var]).copy()

fig_map = px.choropleth(
    map_df,
    locations="country_text_id",
    locationmode="ISO-3",
    color=map_var,
    hover_name="country_name",
    color_continuous_scale=[
        [0.00, "#67001f"],
        [0.20, "#d6604d"],
        [0.40, "#f4a582"],
        [0.50, "#e8e8e8"],
        [0.65, "#92c5de"],
        [0.80, "#4393c3"],
        [1.00, "#2d004b"],
    ],
    range_color=[0, 1],
    labels={map_var: comp_index_label},
    title=f"{comp_index_label} ({comp_year})",
    height=500,
)
fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="",
        tickvals=[0, 0.25, 0.5, 0.75, 1],
        ticktext=["0", "0.25", "0.5", "0.75", "1"],
        len=0.5,
    ),
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth",
        showland=True,
        landcolor="#f0f0f0",
    ),
    margin=dict(t=50, b=0, l=0, r=0),
)
st.plotly_chart(fig_map, use_container_width=True)
st.caption("O índice e o ano exibidos no mapa são controlados pelos seletores 'Índice - comparação e mapa' e 'Ano - comparação e mapa' na barra lateral.")

st.divider()
''

col_radar, col_rank = st.columns([1, 1], gap="large")

with col_radar:
    st.subheader("Perfil democrático do Brasil")
    radar_year = st.select_slider(
        "Ano do perfil",
        options=sorted(brazil["year"].unique()),
        value=2024,
    )

    radar_vars_labels = [
        "Democracia Liberal", "Democracia Eleitoral", "Democracia Participativa",
        "Democracia Igualitária", "Democracia Deliberativa",
        "Liberdade de Expressão", "Eleições Livres e Justas",
        "Estado de Direito", "Sociedade Civil", "Empoderamento Feminino",
    ]
    radar_vars = [INDICES[l] for l in radar_vars_labels]
    row = brazil[brazil["year"] == radar_year].iloc[0]
    values = [row[v] for v in radar_vars] + [row[radar_vars[0]]]
    labels = radar_vars_labels + [radar_vars_labels[0]]

    fig_radar = go.Figure(go.Scatterpolar(
        r=values, theta=labels, fill="toself",
        fillcolor="rgba(0,100,200,0.2)",
        line_color="royalblue",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False, height=420,
        margin=dict(t=30, b=30),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_rank:
    st.subheader("Comparação global")

    comp_var = INDICES[comp_index_label]
    all_countries = ["Brazil"] + comp_countries
    comp_df_plot = df_comp[
        df_comp["country_name"].isin(all_countries) & (df_comp["year"] == comp_year)
    ][["country_name", comp_var]].copy()
    comp_df_plot["País"] = comp_df_plot["country_name"].map(
        lambda x: COUNTRY_PT.get(x, x)
    )
    comp_df_plot = comp_df_plot.sort_values(comp_var, ascending=True)
    comp_df_plot["cor"] = comp_df_plot["country_name"].apply(
        lambda x: "royalblue" if x == "Brazil" else "lightsteelblue"
    )

    fig_bar = px.bar(
        comp_df_plot, x=comp_var, y="País", orientation="h",
        color="cor", color_discrete_map="identity",
        labels={comp_var: comp_index_label, "País": ""},
        height=420, text=comp_df_plot[comp_var].round(3),
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, xaxis_range=[0, 1], margin=dict(t=30))
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()


st.subheader("Tabela de indicadores - Brasil")

table_df = brazil_filtered[["year"] + list(INDICES.values())].copy()
table_df = table_df.rename(
    columns={"year": "Ano", **{v: k for k, v in INDICES.items()}}
)
table_df = table_df.sort_values("Ano", ascending=False).reset_index(drop=True)
for col in table_df.columns[1:]:
    table_df[col] = table_df[col].round(3)

st.dataframe(
    table_df, use_container_width=True, hide_index=True, height=320,
    column_config={"Ano": st.column_config.NumberColumn(format="%d")},
)

with st.expander("Sobre os índices"):
    st.markdown("""
| Índice | Descrição |
|--------|-----------|
| **Democracia Liberal** | Índice síntese que combina dimensão eleitoral com proteção de liberdades individuais e freios ao poder executivo |
| **Democracia Eleitoral** | Mede se eleições são livres, competitivas e com sufrágio universal |
| **Liberdade de Expressão** | Grau de liberdade de imprensa, internet e expressão política |
| **Estado de Direito** | Independência judicial e respeito às leis |
| **Controle da Corrupção** | Accountability horizontal e vertical do governo |
| **Restrições ao Executivo** | Capacidade do legislativo de limitar o executivo |
| **Restrições Judiciais** | Capacidade do judiciário de limitar o executivo |
| **Empoderamento Feminino** | Participação política das mulheres em cargos e eleições |

Todos os indicadores variam de **0** (mínimo) a **1** (máximo democrático).  
Fonte: [V-Dem Project](https://v-dem.net), versão 16 (2026).
""")
