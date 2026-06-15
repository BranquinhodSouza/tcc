"""
Dashboard de Análise de Evasão — PROEJA IFG Goiânia
=====================================================
Para executar: pip install dash pandas plotly
Depois: python dashboard_evasao_python.py
Acessar: http://127.0.0.1:8050
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ========== DADOS ==========
data = {
    "id_aluno": range(1, 51),
    "idade": [24,31,19,45,28,36,22,29,41,33,20,27,38,30,23,42,26,34,21,39,25,37,44,28,35,
              43,32,29,47,41,36,27,20,48,39,35,30,44,48,32,19,26,40,37,33,46,24,38,28,42],
    "sexo": ["M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F",
             "M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F","M","F",
             "M","F","M","F","M","F","M","F","M","F"],
    "raca": ["Pardo","Preta","Branco","Parda","Preto","Branco","Pardo","Preta","Branco","Parda",
             "Preto","Branco","Pardo","Preta","Branco","Parda","Preto","Branco","Pardo","Preta",
             "Branco","Parda","Preto","Branco","Pardo","Preta","Branco","Parda","Preto","Branco",
             "Pardo","Preta","Branco","Parda","Preto","Branco","Pardo","Preta","Branco","Parda",
             "Preto","Branco","Pardo","Preta","Branco","Parda","Preto","Branco","Pardo","Preta"],
    "trabalha": [1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    "possui_filhos": [0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,0,1],
    "curso": ["Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação",
              "Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação",
              "Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação",
              "Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação",
              "Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação","Cozinha","Alimentação"],
    "ingresso": ["2022.1","2022.1","2023.1","2022.2","2023.1","2022.1","2023.2","2023.1","2022.2","2022.1",
                 "2024.1","2023.1","2022.1","2023.2","2022.2","2022.1","2024.1","2023.2","2023.1","2022.2",
                 "2023.2","2022.1","2023.1","2024.1","2022.2","2023.1","2022.1","2022.2","2024.1","2023.1",
                 "2023.2","2022.2","2023.1","2022.1","2024.1","2022.2","2023.1","2022.1","2023.2","2024.1",
                 "2023.1","2022.2","2022.1","2023.1","2023.2","2022.2","2023.1","2023.2","2022.1","2024.1"],
    "status": ["Evadido","Ativo","Evadido","Evadido","Evadido","Ativo","Evadido","Evadido","Formado","Evadido",
               "Evadido","Ativo","Evadido","Evadido","Evadido","Ativo","Evadido","Ativo","Evadido","Evadido",
               "Ativo","Evadido","Evadido","Ativo","Formado","Evadido","Evadido","Ativo","Evadido","Evadido",
               "Ativo","Evadido","Evadido","Formado","Ativo","Evadido","Evadido","Evadido","Ativo","Ativo",
               "Evadido","Evadido","Evadido","Ativo","Evadido","Formado","Evadido","Ativo","Evadido","Ativo"],
    "meses_cursados": [6,48,3,6,12,48,3,6,36,6,3,30,18,6,6,42,3,24,3,6,24,6,6,12,36,
                       6,12,30,3,12,18,6,3,36,12,6,12,6,18,12,6,3,18,24,6,36,3,18,24,12],
    "motivo": ["Trabalho","","Desinteresse","Trabalho","Currículo","","Trabalho","Pessoal/Família","","Trabalho",
               "Pessoal/Família","","Trabalho","Trabalho","Currículo","","Trabalho","","Trabalho","Pessoal/Família",
               "","Trabalho","Currículo","","","Trabalho","Trabalho","","Trabalho","Pessoal/Família",
               "","Trabalho","Desinteresse","","","Trabalho","Currículo","Trabalho","","",
               "Desinteresse","Trabalho","Trabalho","","Trabalho","","Trabalho","","Currículo",""]
}

df = pd.DataFrame(data)
df["faixa_etaria"] = pd.cut(df["idade"], bins=[0, 25, 35, 45, 100], labels=["18-25", "26-35", "36-45", "46+"])
df["trabalha_label"] = df["trabalha"].map({1: "Sim", 0: "Não"})
df["possui_filhos_label"] = df["possui_filhos"].map({1: "Sim", 0: "Não"})

# ========== DASH ==========
app = Dash(__name__)
app.title = "Dashboard Evasão PROEJA IFG"

app.layout = html.Div([
    html.H1("📊 Dashboard de Evasão — PROEJA IFG Goiânia",
            style={"textAlign": "center", "color": "#1a1a2e", "marginBottom": 20}),

    html.Div([
        html.Div([
            html.Label("Curso:"),
            dcc.Dropdown(id="filtro_curso", options=[{"label": "Todos", "value": "todos"}] +
                [{"label": c, "value": c} for c in df["curso"].unique()], value="todos")
        ], style={"width": "22%", "display": "inline-block", "marginRight": "2%"}),
        html.Div([
            html.Label("Sexo:"),
            dcc.Dropdown(id="filtro_sexo", options=[{"label": "Ambos", "value": "todos"},
                {"label": "Masculino", "value": "M"}, {"label": "Feminino", "value": "F"}], value="todos")
        ], style={"width": "22%", "display": "inline-block", "marginRight": "2%"}),
        html.Div([
            html.Label("Trabalha:"),
            dcc.Dropdown(id="filtro_trabalha", options=[{"label": "Todos", "value": "todos"},
                {"label": "Sim", "value": 1}, {"label": "Não", "value": 0}], value="todos")
        ], style={"width": "22%", "display": "inline-block", "marginRight": "2%"}),
        html.Div([
            html.Label("Status:"),
            dcc.Dropdown(id="filtro_status", options=[{"label": "Todos", "value": "todos"},
                {"label": "Ativo", "value": "Ativo"}, {"label": "Evadido", "value": "Evadido"},
                {"label": "Formado", "value": "Formado"}], value="todos")
        ], style={"width": "22%", "display": "inline-block"}),
    ], style={"marginBottom": 20, "padding": "10px", "background": "#f8f9fa", "borderRadius": 8}),

    html.Div(id="kpis", style={"display": "flex", "gap": 15, "marginBottom": 20}),

    html.Div([
        html.Div([dcc.Graph(id="graf_curso")], className="six columns"),
        html.Div([dcc.Graph(id="graf_motivos")], className="six columns"),
    ], className="row", style={"marginBottom": 20}),

    html.Div([
        html.Div([dcc.Graph(id="graf_idade")], className="six columns"),
        html.Div([dcc.Graph(id="graf_sexo_trab")], className="six columns"),
    ], className="row", style={"marginBottom": 20}),

    html.Div([dcc.Graph(id="graf_serie")], style={"marginBottom": 20}),

], style={"maxWidth": 1400, "margin": "0 auto", "padding": 20})

@app.callback(
    [Output("kpis", "children"),
     Output("graf_curso", "figure"),
     Output("graf_motivos", "figure"),
     Output("graf_idade", "figure"),
     Output("graf_sexo_trab", "figure"),
     Output("graf_serie", "figure")],
    [Input("filtro_curso", "value"),
     Input("filtro_sexo", "value"),
     Input("filtro_trabalha", "value"),
     Input("filtro_status", "value")]
)
def update(f_curso, f_sexo, f_trabalha, f_status):
    d = df.copy()
    if f_curso != "todos": d = d[d["curso"] == f_curso]
    if f_sexo != "todos": d = d[d["sexo"] == f_sexo]
    if f_trabalha != "todos": d = d[d["trabalha"] == f_trabalha]
    if f_status != "todos": d = d[d["status"] == f_status]

    total = len(d)
    evadidos = len(d[d["status"] == "Evadido"])
    ativos = len(d[d["status"] == "Ativo"])
    taxa = round(evadidos / total * 100, 1) if total else 0
    tempo = round(d[d["status"] == "Evadido"]["meses_cursados"].mean(), 1)

    kpis = html.Div([
        html.Div([html.Div(f"{taxa}%", style={"fontSize": 32, "fontWeight": 700}),
                   html.Div("Taxa de Evasão", style={"color": "#888"})],
                  style={"flex": 1, "textAlign": "center", "background": "white", "padding": 20, "borderRadius": 12, "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div([html.Div(str(evadidos), style={"fontSize": 32, "fontWeight": 700}),
                   html.Div("Total Evadidos", style={"color": "#888"})],
                  style={"flex": 1, "textAlign": "center", "background": "white", "padding": 20, "borderRadius": 12, "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div([html.Div(str(ativos), style={"fontSize": 32, "fontWeight": 700}),
                   html.Div("Alunos Ativos", style={"color": "#888"})],
                  style={"flex": 1, "textAlign": "center", "background": "white", "padding": 20, "borderRadius": 12, "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
        html.Div([html.Div(str(tempo), style={"fontSize": 32, "fontWeight": 700}),
                   html.Div("Meses até Evasão (média)", style={"color": "#888"})],
                  style={"flex": 1, "textAlign": "center", "background": "white", "padding": 20, "borderRadius": 12, "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
    ], style={"display": "flex", "gap": 15, "width": "100%"})

    # Grafico curso
    aux = d[d["status"] == "Evadido"].groupby("curso").size().reset_index(name="count")
    fig_curso = px.bar(aux, x="curso", y="count", title="Evasão por Curso",
                       color_discrete_sequence=["#d32f2f"], text="count")
    fig_curso.update_layout(yaxis_title="Nº de Evadidos", xaxis_title="")

    # Grafico motivos
    aux = d[d["status"] == "Evadido"]["motivo"].value_counts().reset_index()
    aux.columns = ["motivo", "count"]
    fig_motivos = px.pie(aux, values="count", names="motivo", title="Motivos de Evasão",
                         color_discrete_sequence=px.colors.qualitative.Set2)

    # Grafico idade
    aux = d[d["status"] == "Evadido"].groupby("faixa_etaria", observed=True).size().reset_index(name="count")
    fig_idade = px.bar(aux, x="faixa_etaria", y="count", title="Evasão por Faixa Etária",
                       color_discrete_sequence=["#f57c00"], text="count")
    fig_idade.update_layout(yaxis_title="Evadidos", xaxis_title="")

    # Grafico sexo x trabalho
    aux = d[d["status"] == "Evadido"].groupby(["sexo", "trabalha_label"]).size().reset_index(name="count")
    aux["grupo"] = aux["sexo"] + " - " + aux["trabalha_label"]
    fig_sexo = px.bar(aux, x="grupo", y="count", title="Evasão por Sexo e Situação de Trabalho",
                      color_discrete_sequence=["#1976d2"], text="count")
    fig_sexo.update_layout(yaxis_title="Evadidos", xaxis_title="")

    # Serie historica
    semestres_ordem = ["2022.1", "2022.2", "2023.1", "2023.2", "2024.1"]
    serie = d.groupby("ingresso").agg(total=("id_aluno", "count"),
                                       evadidos=("status", lambda x: (x == "Evadido").sum())).reset_index()
    serie["taxa"] = (serie["evadidos"] / serie["total"] * 100).round(1)
    fig_serie = px.line(serie, x="ingresso", y="taxa", title="Taxa de Evasão por Semestre de Ingresso",
                        markers=True, range_y=[0, 80])
    fig_serie.update_traces(line_color="#d32f2f", line_width=3)
    fig_serie.update_layout(yaxis_title="Taxa (%)", xaxis_title="", yaxis_ticksuffix="%")

    return kpis, fig_curso, fig_motivos, fig_idade, fig_sexo, fig_serie

if __name__ == "__main__":
    print("=" * 55)
    print("Dashboard de Evasão — PROEJA IFG Goiânia")
    print("=" * 55)
    print("\nPara instalar as dependências:")
    print("  pip install dash pandas plotly")
    print("\nApós instalar, execute:")
    print("  python dashboard_evasao_python.py")
    print("  Acesse: http://127.0.0.1:8050")
    print("\n" + "=" * 55)
    app.run(debug=True)
