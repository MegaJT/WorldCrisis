import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import dash
import pandas as pd
from datetime import datetime
from components.get_components_home import create_card, create_accordion


dash.register_page(__name__, path="/", order=0)

########data prep ###################
# post process original dataset
data = pd.read_csv("./data/data_2024.csv")
# summary statistics and support variables for sliding card
stat_start_date = datetime(2024, 1, 1)
stat_end_date = datetime(2024, 5, 31)
stat_duration = (stat_end_date - stat_start_date).days

civ_deaths_sum = data["deaths_civilians"].sum()
civ_deaths_rate = int(civ_deaths_sum / stat_duration)
country_count = data.country.nunique()
conflicts_count = data.conflict_new_id.nunique()

##### sliding cards and  navigation accordion #########
# build components with custom functions
card1 = create_card("LOGO.png", f"{conflicts_count} Active conflicts worldwide")
card2 = create_card("LOGO.png", f"{country_count} Countries in a war situation")
card3 = create_card("LOGO.png", f"{civ_deaths_sum} Civilian casualities")
card4 = create_card("LOGO.png", f" {civ_deaths_rate} Civilian casualties every day")
accordion = create_accordion()

# main page container
layout = dbc.Container(
    [
        # interval component for sliding card timing control
        dcc.Interval(
            id="card_interval-id",
            disabled=False,
            n_intervals=0,
            interval=1 * 4000,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [card1],
                    id="card-id",
                    width=12,
                ),
            ],
            className="my-4 ",
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Container(
                        [
                            html.Hr(),
                            html.H4(
                                [
                                    "Learn through data on global conflict zones and civilian casualties in early 2024 "
                                ],
                                className="text-primary fw-bold m-3 d-flex justify-content-center ",
                            ),
                        ],
                    )
                ]
            )
        ),
        dbc.Row(
            [
                dbc.Col([], width=1),
                dbc.Col(
                    [
                        dbc.Container(
                            accordion,
                            fluid=False,
                        ),
                    ],
                    width=10,
                ),
                dbc.Col([], width=1),
            ],
            align="center",
            className="mb-5 p-5",
        ),
        html.Hr(),
    ]
)


# run sliding cards
@callback(
    Output("card-id", "children"),
    [
        Input("card_interval-id", "n_intervals"),
    ],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def change_page(num):
    pageMap = {
        key: value
        for key, value in zip([f"k{i}" for i in range(4)], [card1, card2, card3, card4])
    }
    page = num % 4
    currentCard = pageMap[f"k{page}"]

    return currentCard
