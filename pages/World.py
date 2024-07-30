import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np

dash.register_page(__name__, path="/World", order=1)


################ data prep#########################
# get post-proc dataset
data = pd.read_csv("./data/data_2024.csv")
# retrive countries geometries, locations ids (iso-alpha codes) ---> original data source from kaggle
# Opening JSON file
f = open("./data/world-countries.json")
# returns JSON object as
# a dictionary
geoj = json.load(f)

#####
data_agg = (
    data.groupby(by=["country", "iso_alpha"])[["best", "deaths_civilians"]]
    .sum()
    .reset_index()
)
data_agg["best_log"] = np.log10(data_agg.best + 1)
data_agg["deaths_civilians_log"] = np.log10(data_agg.deaths_civilians + 1)

######
# choropleth map - world level. color by civilians death per country. Data aggregated on weekly basis
# to shrink color scale, eval "log"
# both statics and animated version mpas implemented
# sort data by date - this to guarantee correct animation sequency
data_agg_weekly = (
    data.groupby(by=["country", "iso_alpha", "date_start_wymd", "region"])[
        ["best", "deaths_civilians"]
    ]
    .sum()
    .reset_index()
)
# extra time stamps needed for different vizs
data_agg_weekly["best_log"] = np.log(data_agg_weekly.best + 1)
data_agg_weekly["deaths_civilians_log"] = np.log(data_agg_weekly.deaths_civilians + 1)
data_agg_weekly["date_start_wymd"] = pd.to_datetime(
    data_agg_weekly["date_start_wymd"]
).dt.strftime("%Y-%m-%d")
data_agg_weekly.sort_values(by=["date_start_wymd"], inplace=True)
data_agg_weekly.reset_index(drop=True, inplace=True)

################color sequence #####################
# custom color sequence to keep same style for different plots
region_dict = {
    "Europe": "#18a2ee",
    "Asia": "#AFDCEC",
    "Africa": "#6960EC",
    "Middle East": "#316c94",
    "Americas": "#2f4050",
}

#################### vizs ##################################################
## world page have two plots. A map at the top.
##Bottom plot can change according to the user settings and controls status
## plots update via callback

## default top plot - main map -static version ###

fig1 = px.choropleth_mapbox(
    data_agg,
    locations="iso_alpha",
    color="deaths_civilians_log",
    geojson=geoj,
    color_continuous_scale=px.colors.sequential.ice_r[2:],
    mapbox_style="carto-positron",
    zoom=1,
    opacity=0.5,
    hover_name="country",
    hover_data=["deaths_civilians", "best"],
    animation_frame=None,
    animation_group=None,
    height=550,
)
fig1.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="Deaths",
        tickvals=[0, 1, 2, 3, 4, 5],
        ticktext=["1", "10", "100", "1k", "10k", "100k"],
    ),
)
fig1.update_traces(marker_line_width=0)
fig1.update_coloraxes(
    colorbar_orientation="h",
)
fig1.update_layout(coloraxis_colorbar_y=-0.2)

## default bottom plot
fig2 = px.histogram(
    data,
    x="region",
    y="deaths_civilians",
    color="region",
    hover_name="country",
    height=300,
    color_discrete_map=region_dict,
)

fig2.update_layout(xaxis={"categoryorder": "total descending"})

##### top main map control panel ####
# user can switch between overall data summary and weekly aggregation
button_group = html.Div(
    [
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary border-0 shadow ",
            labelCheckedClassName="active",
            options=[
                {"label": "Overall", "value": 1},
                {"label": "Weekly", "value": 2},
            ],
            value=1,
        ),
    ],
    className="radio-group",
)

## container for all main plots and components
world_overall_container = dbc.Container(
    [
        dbc.Row(dbc.Col([button_group])),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H4(
                                    ["Deaths Civilians Cases Map"],
                                    className="text-primary mt-3 ms-3 me-3 fw-bold",
                                ),
                                dcc.Graph(
                                    id="fig1",
                                    figure=fig1,
                                ),
                            ],
                            className="m-3 border-light shadow",
                        )
                    ],
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Container(
                                [
                                    html.H4(
                                        ["Deaths Civilians by Geographic Area "],
                                        className="text-primary mt-3 ms-3 me-3 fw-bold",
                                        id="title-aggr",
                                    ),
                                    dcc.Graph(
                                        id="fig2",
                                        figure=fig2,
                                        className=" border-light",
                                    ),
                                    # pagination to navigate across avaiable plots
                                    dbc.Pagination(
                                        max_value=2,
                                        id="pagination-world",
                                    ),
                                ],
                                className="border-light shadow  border-0 ",
                            )
                        ],
                        className="mt-1 mx-3 mb-1 border-light",
                    )
                ),
            ],
        ),
    ],
    className="my-4",
    id="map-container",
)


##### page container ###############
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        ["Worldwide Overview"],
                        className="text-primary fw-bold mt-3 ms-3",
                    ),
                    dbc.Button(
                        html.I(className="bi bi-info-circle-fill mt-3  fs-3"),
                        id="collapse-button-world",
                        className="m-3 text-primary border-0",
                        color="light",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Markdown(
                                    [
                                        """Civilians deaths summary in 2024 Jan-May conflics.  
                                    Overall and weekly aggregated data options available.  
                                    Multiple visualizations avaialable through the controls."""
                                    ],
                                    className="text-primary",
                                )
                            )
                        ),
                        id="collapse-world",
                        is_open=False,
                    ),
                ],
                style={
                    "display": "flex",
                    "align-self": "start",
                    "justify-content": "flex-start",
                },
            )
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col([dbc.Container([world_overall_container], id="container-world")]),
        ),
    ]
)


##callback to switch from static overall map (default) to animated version with weekly data
@callback(
    Output("fig1", "figure"),
    [
        Input("radios", "value"),
    ],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def animated_map(value):

    animation_frame = None
    animation_group = None
    mapbox_style = "carto-positron"
    data_map = data_agg
    colorbar = dict(
        title="Deaths",
        tickvals=[0, 1, 2, 3, 4, 5],
        ticktext=["1", "10", "100", "1k", "10k", "100k"],
    )
    val_y = -0.2

    if value == 2:
        print("active anim")
        animation_frame = "date_start_wymd"
        animation_group = "country"
        mapbox_style = "carto-positron"
        data_map = data_agg_weekly
        colorbar = dict(
            title="Deaths",
            tickvals=[],
            ticktext=[],
        )
        val_y = -0.1

    fig1 = px.choropleth_mapbox(
        data_map,
        locations="iso_alpha",
        color="deaths_civilians_log",
        geojson=geoj,
        color_continuous_scale=px.colors.sequential.ice_r[2:],
        mapbox_style=mapbox_style,
        zoom=1,
        opacity=0.5,
        hover_name="country",
        hover_data=["deaths_civilians", "best"],
        animation_frame=animation_frame,
        animation_group=animation_group,
        height=550,
    )
    fig1.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_colorbar=colorbar
    )
    fig1.update_traces(marker_line_width=0)
    fig1.update_coloraxes(
        colorbar_orientation="h",
    )
    fig1.update_layout(coloraxis_colorbar_y=val_y)

    fig1.update_layout(mapbox_style="carto-positron")
    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig1


##callback to control bottom plots - switch from overall summary barchart/hist (default) to weekly data vizs (line/barchart)
@callback(
    [Output("fig2", "figure"), Output("title-aggr", "children")],
    [Input("radios", "value"), Input("pagination-world", "active_page")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def main_chart(r_value, p_value):
    fig2 = ""
    title = ""

    if r_value == 2:
        title = "Deaths Civilians by Week"
        if p_value == 2:
            fig2 = px.bar(
                data_agg_weekly.groupby(by=["date_start_wymd", "region"])[
                    ["best", "deaths_civilians"]
                ]
                .sum()
                .reset_index(),
                x="date_start_wymd",
                y="deaths_civilians",
                color="region",
                color_discrete_map=region_dict,
                height=300,
            )

        else:
            fig2 = px.line(
                data_agg_weekly.groupby(by=["date_start_wymd"])[
                    ["best", "deaths_civilians"]
                ]
                .sum()
                .reset_index(),
                x="date_start_wymd",
                y="deaths_civilians",
                markers=True,
                height=300,
                color_discrete_sequence=px.colors.qualitative.G10,
            )
            fig2.update_traces(marker={"size": 15})
    else:
        title = "Deaths Civilians by Geographic Area"
        if p_value == 2:
            fig2 = px.bar(
                data.groupby(by=["country", "date_start_wymd", "region"])[
                    "deaths_civilians"
                ]
                .sum()
                .reset_index(),
                x="country",
                y="deaths_civilians",
                color="region",
                hover_name="country",
                color_discrete_map=region_dict,
            )

            fig2.update_layout(xaxis={"categoryorder": "total descending"})
            # Add range slider
            fig2.update_layout(
                xaxis_rangeslider_visible=True,
                xaxis_range=[0, 10],
                xaxis_rangeslider_thickness=0.02,
            )
            fig2.update_layout(
                margin={
                    "r": 0,
                    "l": 0,
                }
            )
        else:
            fig2 = px.histogram(
                data,
                x="region",
                y="deaths_civilians",
                color="region",
                # histfunc="sum",
                hover_name="country",
                height=300,
                color_discrete_map=region_dict,
            )

    return fig2, title


##callback to control collapse component with user guide info
@callback(
    Output("collapse-world", "is_open"),
    [Input("collapse-button-world", "n_clicks")],
    [State("collapse-world", "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
