import dash_bootstrap_components as dbc
import dash
from dash import html, dcc


##support custom function to build cards for countries page
def create_card_country(img, title="", value="", note="", id=""):
    card = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            title,
                                            className="card-title card-text text-primary fw-bold",
                                        ),
                                        html.H4(
                                            value,
                                            className="card-text text-primary fw-bold",
                                            id=f"{id}-value",
                                        ),
                                        html.Small(
                                            note,
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-12 text-center",
                            ),
                        ],
                        className="align-items-center",
                        align="center",
                    )
                ],
                className="mb-3 bg-opacity-10  mt-3 shadow my-2 bg-primary  rounded border-0  ",
                id=id,
            ),
        ],
        className="",
    )

    return card
