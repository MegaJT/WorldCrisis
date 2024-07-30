import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ctx, State
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from components.get_components_country import create_card_country
from utils.settings import getEnvVar

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


#
# env var for openAI api call
API_KEY = getEnvVar()

dash.register_page(__name__, path="/Countries", order=2)

###data prep #####
################ data prep#########################
# get post-proc dataset
data = pd.read_csv("./data/data_2024.csv")
data["event"] = 0
# retrive countries geometries, locations ids (iso-alpha codes) ---> original data source from kaggle
# Opening JSON file
f = open("./data/world-countries.json")
# returns JSON object as
# a dictionary
geoj = json.load(f)

###components####
# country selector
country_items = [country for country in data.country.unique().tolist()]
country_dropdown = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Dropdown(
                    options=country_items,
                    value=country_items[0],
                    id="country-dropdown",
                    clearable=False,
                    style={"width": "50%"},
                ),
            ],
            style={
                "display": "flex",
                "align-self": "start",
                "justify-content": "flex-start",
            },
        ),
    ],
)

# language selector
langList = ["English", "French", "Spanish", "Hindi", "Italian", "Portoguese", "Chinese"]
langMenu = dcc.Dropdown(
    options=langList,
    value=langList[0],
    id="input",
    clearable=False,
    className=" m-1  text-primary  bg-secondary rounded bg-opacity-10 shadow justify-content-center",
)

#### default visz
## world page have two plots. A map at the top showing event location. Scatter plots showing events timeline.
# both plots focused on civilians death
##bottom plots can show violent attack dates overlapped to the civilian deaths. Overlap controlled by radio button
## plots updates via callback

## default top plot - main map -selected countries events ###
fig3 = px.scatter_mapbox(
    data[data.country == country_items[0]],
    lat="latitude",
    lon="longitude",
    color="deaths_civilians",
    hover_name="country",
    size="deaths_civilians",
    zoom=3,
    height=350,
    center={
        "lat": data[data.country == country_items[0]].latitude.values[0],
        "lon": data[data.country == country_items[0]].longitude.values[0],
    },
    color_continuous_scale=px.colors.sequential.ice_r[2:],
    template="ggplot2",
)

fig3.update_layout(mapbox_style="carto-positron")
fig3.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 10})
fig3.update_coloraxes(
    colorbar_orientation="v",
)
fig3.update_layout(
    coloraxis_colorbar_x=0.95,
    coloraxis_colorbar=dict(title="Deaths"),
)

## default bottom plot - scatter plot. ###
fig4 = px.scatter(
    data[data.country == country_items[0]],
    x="date_start",
    y="deaths_civilians",
    color="deaths_civilians",
    size="deaths_civilians",
    color_continuous_scale=px.colors.sequential.ice_r[2:],
    template="ggplot2",
    height=400,
)

fig4.update_layout(margin={"r": 0, "l": 0, "b": 0, "t": 10})
fig4.update_coloraxes(showscale=False)
fig4.update_layout(showlegend=True)

##calculated variable to populate the summary cards###
case_count = data[data.country == country_items[0]].shape[0]
death_civ_count = data[(data.country == country_items[0])]["deaths_civilians"].sum()
best_count = data[(data.country == country_items[0])]["best"].sum()
## build summary card with custom functions
case_card = create_card_country("", f"{case_count} attacks", id="case-card")
death_civ_card = create_card_country(
    "", f"{death_civ_count} civilian casualties", id="death-civ-card"
)
death_total_card = create_card_country(
    "", f"{best_count} total deaths", id="death-total-card"
)
##container for card placement
card_country_cointainer = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([case_card], width=3),
                dbc.Col([death_civ_card], width=3),
                dbc.Col([death_total_card], width=3),
            ],
            justify="evenly",
        ),
    ],
    id="card-country-container",
)
## other components ####
button_group_country = html.Div(
    [
        dbc.RadioItems(
            id="radios_country",
            className="btn-group ",
            inputClassName="btn-check ",
            labelClassName="btn btn-outline-primary border-0 shadow  ",
            labelCheckedClassName="active",
            options=[
                {"label": "Show Attacks", "value": 2},
                {"label": "reset", "value": 1},
            ],
            value=1,
        ),
    ],
    className="radio-group ",
)

## container for all main plots and components
country_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(country_dropdown),
                dbc.Col(
                    [
                        dbc.Offcanvas(
                            dcc.Loading(
                                dbc.Container(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.H5(
                                                        [
                                                            "Select a data point to get event headlines. AI assisted features. English default language."
                                                        ],
                                                        id="testAI",
                                                        className="text-primary  ",
                                                    ),
                                                ],
                                                width=10,
                                                class_name="p-2  bg-primary bg-opacity-10",
                                            )
                                        ],
                                        className="d-flex justify-content-center",
                                    ),
                                )
                            ),
                            id="offcanvas-scrollable",
                            scrollable=True,
                            is_open=False,
                            placement="bottom",
                            backdrop=False,
                            className="m-3 pt-35 text-primary fw-bold ",
                            style={
                                "height": "300px",
                            },
                        ),
                    ]
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col([case_card], width=3),
                                dbc.Col([death_total_card], width=3),
                                dbc.Col([death_civ_card], width=3),
                            ],
                            justify="evenly",
                        ),
                    ],
                    id="card-country-container",
                )
            ]
        ),
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
                                    id="fig3",
                                    figure=fig3,
                                ),
                            ],
                            className="m-3 border-light shadow",
                        )
                    ],
                    # width=8,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4(
                                ["Deaths Civilians Timeseries"],
                                className="text-primary mt-3 ms-3 me-3 fw-bold",
                            ),
                            dbc.Container(
                                [
                                    dcc.Graph(
                                        id="fig4",
                                        figure=fig4,
                                        className="border-light ",
                                    ),
                                ],
                            ),
                        ],
                        className=" m-3 border-light shadow",
                    )
                ),
            ],
        ),
        dbc.Row(button_group_country),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            html.H5(
                                [
                                    "Select a data point to get event headlines. AI assisted features.",
                                    html.Br(),
                                    "Default Language English. Use the input field to update the language settings.",
                                ],
                                id="NoteAI",
                                className="mt-3  text-primary  ",
                            )
                        ),
                    ],
                    width=10,
                    className="m-3 pt-35 text-primary fw-bold bg-primary rounded bg-opacity-10 shadow justify-content-center",
                )
            ],
            align="center",
            style={
                "display": "flex",
                "align-self": "center",
                "justify-content": "space-around",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    [langMenu],
                    width=10,
                    className=" shadow justify-content-center",
                )
            ],
            align="center",
            style={
                "display": "flex",
                "align-self": "center",
                "justify-content": "space-around",
            },
        ),
        html.Hr(),
    ],
    className="my-4",
    id="map-container",
)

# page container
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            ["Countries Explorer"],
                            className="text-primary fw-bold mt-3 ms-3",
                        ),
                        dbc.Button(
                            html.I(className="bi bi-info-circle-fill mt-3  fs-3"),
                            id="collapse-button",
                            className="m-3 text-primary border-0",
                            color="light",
                            n_clicks=0,
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    dcc.Markdown(
                                        [
                                            """Civilians deaths summary in 2024 Jan-May conflics by country.    
                                    Selected country maps and weekly aggregated data reported.  
                                    Attacks makers overlay the death civilians trend on demand.   
                                    AI assisted events description by clicking makers on the charts.  
                                    Language preference inputs at the bottom of the page."""
                                        ],
                                        className="text-primary",
                                    )
                                )
                            ),
                            id="collapse",
                            is_open=False,
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-self": "start",
                        "justify-content": "flex-start",
                    },
                ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col([dbc.Container([country_container], id="container-country")]),
        ),
    ]
)


# callback to control plots and card data according to the selected country
# radio button status control the overlay of the attacks timeline to the deaths civilans timeseries
@callback(
    [
        Output("fig3", "figure"),
        Output("fig4", "figure"),
        Output("card-country-container", "children"),
    ],
    Input("country-dropdown", "value"),
    Input("radios_country", "value"),
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def country_vizs(value, radioVal):
    fig3 = px.scatter_mapbox(
        data[data.country == value],
        lat="latitude",
        lon="longitude",
        color="deaths_civilians",
        hover_name="country",
        size="deaths_civilians",
        zoom=3,
        height=300,
        center={
            "lat": data[data.country == value].latitude.values[0],
            "lon": data[data.country == value].longitude.values[0],
        },
        color_continuous_scale=px.colors.sequential.ice_r[2:],
        template="ggplot2",
    )
    fig3.update_layout(mapbox_style="carto-positron")
    fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig3.update_coloraxes(
        colorbar_orientation="v",
    )
    fig3.update_layout(
        coloraxis_colorbar_x=0.95,
        coloraxis_colorbar=dict(title="Deaths"),
    )

    fig4 = px.scatter(
        data[data.country == value],
        x="date_start",
        y="deaths_civilians",
        color="deaths_civilians",
        size="deaths_civilians",
        color_continuous_scale=px.colors.sequential.ice_r[2:],
        template="ggplot2",
    )

    fig4.update_coloraxes(showscale=False)
    if radioVal == 2:
        fig4.add_traces(
            px.scatter(
                data[data.country == value],
                x="date_start",
                y="event",
                symbol_sequence=["x-dot"],
            ).data,
        )
    fig4.update_layout(showlegend=True)

    # card content update
    case_count = data[data.country == value].shape[0]
    death_civ_count = data[(data.country == value)]["deaths_civilians"].sum()
    case_card = create_card_country("", f"{case_count} attacks")
    death_civ_card = create_card_country("", f"{death_civ_count} civilian casualties")
    best_count = data[(data.country == value)]["best"].sum()

    death_total_card = create_card_country(
        "", f"{best_count} total deaths", id="death-total-card"
    )

    card_country_cointainer = [
        dbc.Row(
            [
                dbc.Col([case_card], width=3),
                dbc.Col([death_total_card], width=3),
                dbc.Col([death_civ_card], width=3),
            ],
            justify="evenly",
        )
    ]

    return fig3, fig4, card_country_cointainer


# AI assisted summary of the headlines from the dataset.
# LLE prompt built on the basis of the clicked data on the maps or scatterplots
# the user selected language.
# offcanvas opened to show LLM response.
@callback(
    [
        Output("testAI", "children"),
        Output("offcanvas-scrollable", "is_open"),
        Output("NoteAI", "children"),
    ],
    [Input("fig3", "clickData"), Input("fig4", "clickData")],
    [
        State("country-dropdown", "value"),
        State("offcanvas-scrollable", "is_open"),
        State("input", "value"),
    ],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def info_onClick(f1clickedData, f2clickedData, value, is_open, inputVal):
    triggerID = ctx.triggered_id
    if triggerID == "fig3":
        clickedData = f1clickedData
    else:
        clickedData = f2clickedData

    # print(clickedData)
    if clickedData is not None:
        status_canvas = not is_open
    noteAI = (
        "Select a data point to get event headlines. AI assisted features.",
        html.Br(),
        "Default Language English. Use the input field to update the language settings.",
    )

    if inputVal is None:
        language = "English"
    else:
        language = str(inputVal)

    data_temp = data[data.country == value].reset_index()
    source_headlines = data_temp.source_headline.loc[
        clickedData["points"][0]["pointNumber"]
    ]
    data_start = (
        data_temp["date_start"].astype(str).loc[clickedData["points"][0]["pointNumber"]]
    )
    country = data_temp["country"].loc[clickedData["points"][0]["pointNumber"]]

    ##LLM prompt template
    prompt_template = PromptTemplate.from_template(
        """  Please summarize in {language} what happened in {countrysel} on {datastart} by usign the following headilines: {sourceheadline}. 
        In case of multiple headlines they are separated by semicolon. Use a serious reporter tone.
          Start your summary by mentioning {countrysel} name and {datastart}. 
        """
    )

    llm = ChatOpenAI(openai_api_key=API_KEY)
    chain = prompt_template | llm
    response = chain.invoke(
        dict(
            language=language,
            countrysel=country,
            datastart=data_start,
            sourceheadline=source_headlines,
        )
    )

    return (
        f"AI: {response.content}",
        status_canvas,
        noteAI,
    )


##callback to control collapse component with user guide info
@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
