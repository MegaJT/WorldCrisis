import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ctx, State
import dash
import pandas as pd
import plotly.express as px
import numpy as np
import dash_ag_grid as dag
import plotly.graph_objects as go


dash.register_page(__name__, path="/Conflictsindex", order=3)

###### data preparation ################
# original dataset as starting point to build the conflict index (KPI)
# main index components are the countries attacks rate, civilians deaths deaths rate and overall death rate
# components rate calculated over a period of 150 days (5 months)
# rate standardization and bias applied to have the three rates components in the same range and
# starting from 1 -->attack_score, deaths_civilians_score, deaths_score
# conflict index is the magnitude of the 3D vector defined for each country from attack_score, deaths_civilians_score, deaths_score
data = pd.read_csv("./data/data_2024.csv")

KPI = (
    data.groupby(by=["country", "region"])[
        ["deaths_a", "deaths_b", "deaths_civilians", "deaths_unknown", "best"]
    ]
    .sum()
    .reset_index()
)
KPI_tmp = data.groupby(by=["country", "region"])[["id"]].count().reset_index()
KPI = KPI.merge(KPI_tmp, on=["country", "region"], how="left")

KPI["rate_civilians"] = KPI["deaths_civilians"] / 150
KPI["rate_best"] = KPI["best"] / 150
KPI["rate_non_civilians"] = KPI["rate_best"] - KPI["rate_civilians"]
KPI["rate_id"] = KPI["id"] / 150
KPI["rate_civilians_std"] = (
    KPI.rate_civilians - KPI.rate_civilians.mean()
) / KPI.rate_civilians.std()
KPI["rate_best_std"] = (KPI.rate_best - KPI.rate_best.mean()) / KPI.rate_best.std()
KPI["deaths_score"] = KPI["rate_best_std"] - KPI["rate_best_std"].min() + 1
KPI["rate_id_std"] = (KPI.rate_id - KPI.rate_id.mean()) / KPI.rate_id.std()
KPI["attacks_score"] = KPI["rate_id_std"] - KPI["rate_id_std"].min() + 1
KPI["deaths_civilians_score"] = (
    KPI["rate_civilians_std"] - KPI["rate_civilians_std"].min() + 1
)
KPI["conflicts_index"] = np.sqrt(
    (KPI.deaths_score) ** 2
    + (KPI.attacks_score) ** 2
    + (KPI.deaths_civilians_score) ** 2
).round(3)
KPI = (
    KPI.sort_values(by="conflicts_index", ascending=False)
    .reset_index()
    .drop(columns="index")
)

##index guide
indexGuide = dcc.Markdown(
    [
        """Conflict Index is a synthetic index for relative conflicts comparison.  
    Its value is calculated by considering the rate of the attacks, civilian deaths and overall deaths for a given country.  
    Standardization  and bias applied to have the score components in the same range starting from one.  
    The index value is calculated for each country as the lenght of the vector in the 3-D space defined by death_score, deaths_civilans_score and attacks_score.  
    """
    ]
)
#### table ####
# summary table prep. For each countries, conflicts index and each components reported
# data sorted by conflict index. the first 3 countries selected by default. this is to
# initially populated the plots:
# barchart showing conflicts index for the selected countries and a radar chart showing the 3 components.
columnDefs = [
    {
        "field": "country",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
    },
    {"headerName": "Region", "field": "region"},
    {
        "headerName": "conflicts_index",
        "field": "conflicts_index",
        "type": "leftAligned",
        "valueFormatter": {"function": "d3.format(',.3f')(params.value)"},
        "filter": None,
    },
    {
        "headerName": "deaths_civilians_score",
        "field": "deaths_civilians_score",
        "type": "leftAligned",
        "valueFormatter": {"function": "d3.format('.3f')(params.value)"},
        "filter": None,
    },
    {
        "headerName": "deaths_score",
        "field": "deaths_score",
        "type": "leftAligned",
        "valueFormatter": {"function": "d3.format(',.3f')(params.value)"},
        "filter": None,
    },
    {
        "headerName": "attack_score",
        "field": "attacks_score",
        "type": "leftAligned",
        "valueFormatter": {"function": "d3.format(',.3f')(params.value)"},
        "filter": None,
    },
]

# page main container
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            ["Conflicts index"],
                            className="text-primary fw-bold mt-3 ms-3",
                        ),
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            [
                                "Synthetic index summarizing three indicators: attack rate, overall deaths rate and civilians death rate."
                            ],
                            className="text-primary  ",
                        ),
                        dbc.Button(
                            "More about the Conflict Index",
                            # html.I(className="bi bi-info-circle-fill mt-3  fs-3"),
                            id="collapse-button-index",
                            className="m-3 text-light border-0",
                            color="primary",
                            n_clicks=0,
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody([indexGuide], className="text-primary  ")
                            ),
                            id="collapse-index",
                            is_open=False,
                            # dimension="width",
                        ),
                    ],
                    width=10,
                    class_name="m-2 p-3  bg-primary bg-opacity-10 shadow",
                )
            ],
            className="d-flex justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.H4(
                                    ["Countries Conflict Index and Rate Components"],
                                    className="text-primary mt-2 mb-2 ms-3 me-3 fw-bold",
                                ),
                                dbc.Button(
                                    html.I(className="bi bi-info-circle-fill  fs-3"),
                                    id="collapse-button-table",
                                    className="text-primary border-0",
                                    color="light",
                                    n_clicks=0,
                                ),
                                dbc.Collapse(
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Markdown(
                                                [
                                                    """Select table entries for countries comparison. Visualization updated accordingly."""
                                                ],
                                                className="text-primary",
                                            )
                                        )
                                    ),
                                    id="collapse-table",
                                    is_open=False,
                                    # dimension="width",
                                ),
                            ],
                            className="mt-3",
                            style={
                                "display": "flex",
                                "align-self": "start",
                                "justify-content": "flex-start",
                            },
                        ),
                        dag.AgGrid(
                            id="crossfilter-example",
                            rowData=KPI.to_dict("records"),
                            columnDefs=columnDefs,
                            defaultColDef={
                                "resizable": True,
                                "sortable": True,
                                "filter": True,
                            },
                            columnSize="sizeToFit",
                            dashGridOptions={
                                "rowSelection": "multiple",
                                # "pagination": True,
                                "animateRows": False,
                                # "paginationPageSize": 10,
                            },
                            className="ag-theme-alpine headers1",
                            selectedRows=KPI.head(3).to_dict("records"),
                        ),
                    ],
                    width=11,
                )
            ],
            justify="evenly",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.H4(
                                    ["Conficts Index by Country"],
                                    className="text-primary mt-3 ms-3 me-3 fw-bold",
                                ),
                                dbc.Container([], id="graph5_container"),
                            ],
                            className="shadow m-3 p-3",
                            style={"background-color": "white"},
                        )
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.H4(
                                    ["Conflicts Index Components by Country"],
                                    className="text-primary mt-3 ms-3 me-3 fw-bold",
                                ),
                                dbc.Container(
                                    ["select Countries from the table"],
                                    id="div-crossfilter-example",
                                ),
                            ],
                            className="shadow m-3 p-3",
                            style={"background-color": "white"},
                        )
                    ],
                    width=5,
                ),
            ],
            className="d-flex justify-content-center",
        ),
    ]
)


# callback to update the visualization given the selected countries in the table
@callback(
    [
        Output("div-crossfilter-example", "children"),
        Output("graph5_container", "children"),
    ],
    Input("crossfilter-example", "virtualRowData"),
    Input("crossfilter-example", "selectedRows"),
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def update_graphs(rows, selected):
    dff = KPI if rows is None else pd.DataFrame(rows)
    theta = ["deaths_civilians_score", "deaths_score", "attacks_score"]
    selected = [s["country"] for s in selected] if selected else []
    print(selected)
    fig6 = go.Figure()
    fig5 = go.Figure()
    graphs = []
    for s in selected:
        r = dff[dff.country == s][theta].values[0]
        # print(r)
        fig6.add_trace(
            go.Scatterpolar(
                r=r,
                theta=theta,
                fill="toself",
                name=s,
            )
        )
        fig6.update_layout(template="ggplot2")

        for column in ["conflicts_index"]:
            if column in dff[dff.country.isin(selected)]:
                fig5 = px.bar(
                    dff[dff.country.isin(selected)],
                    y="country",
                    x=column,
                    # height=250,
                    orientation="h",
                    template="ggplot2",
                )
                fig5.update_traces(marker={"color": "#0074D9"})
                fig5.update_layout(
                    margin={"t": 10, "l": 10, "r": 10},
                    xaxis={"automargin": True, "title": {"text": column}},
                    yaxis={
                        "automargin": True,
                    },
                )
        graphs.append(dcc.Graph(id=column, figure=fig6))
        graphs = [graphs[0]]
        # graph5 = [dcc.Graph(figure=fig5, id="f5")][0]
    return graphs, dcc.Graph(figure=fig5, id="f5")


##callback to control collapse component with user guide info - info about how to use the table
@callback(
    Output("collapse-table", "is_open"),
    [Input("collapse-button-table", "n_clicks")],
    [State("collapse-table", "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


##callback to control collapse component with user guide info --details about conflicts index
@callback(
    Output("collapse-index", "is_open"),
    [Input("collapse-button-index", "n_clicks")],
    [State("collapse-index", "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
