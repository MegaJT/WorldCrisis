import dash_bootstrap_components as dbc
import dash
from dash import html, dcc


##support custom function to build cards and accordion - home page components
def create_card(img, title="", value="", note=""):
    card = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src=dash.get_asset_url(img),
                                    style={"width": "60%"},
                                    className="img-fluid  card-info",
                                ),
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H1(
                                            title,
                                            className="card-title card-text text-primary fw-bold",
                                        ),
                                        html.H1(
                                            value,
                                            className="card-text text-primary fw-bold",
                                        ),
                                        html.Small(
                                            note,
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                        className="align-items-center",
                    )
                ],
                className="mb-3 bg-opacity-10  mt-3 shadow my-2 bg-light  rounded  ",
            ),
            dbc.Card(
                className="mb-3 mt-3 bg-primary shadow my-2",  # bg-opacity-50  ",
                style={"maxWidth": 55},
            ),
        ],
        className="",
    )

    return card


def create_accordion():
    accordion = html.Div(
        [
            html.H2(
                "Discover ",
                className="text-primary fw-bold  ms-5 ",
            ),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P("WorldWide overview of 2024 Jan-May conflics"),
                            dcc.Link("Go to the world data page", href="/World"),
                        ],
                        title="World View",
                        className="bg-opacity-10 me-5  ms-5  mt-3 border-light border-1 bg-light text-primary rounded",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("Country level overview of 2024 Jan-May conflics"),
                            dcc.Link(
                                "Go to the data by country page", href="/Countries"
                            ),
                        ],
                        title="Countries View",
                        className="bg-opacity-10 me-5  ms-5  mt-3 border-light border-1 bg-light text-primary rounded",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Conflicts comparison based on conflicts index, a composit statistics aggregating multiple measurements"
                            ),
                            dcc.Link("Go to the  page", href="/Conflictsindex"),
                        ],
                        title="Conflicts Index",
                        className="bg-opacity-10 me-5  ms-5  mt-3 border-light border-1 bg-light text-primary rounded",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                [
                                    "Under development-to join the ",
                                    dcc.Link(
                                        "Charming Data Community ,",
                                        href="https://charming-data.circle.so/home",
                                        target="_blank",
                                    ),
                                    "Project initiative",
                                ]
                            ),
                            html.P("Original data sources from "),
                            html.Ul(
                                [
                                    html.Li(
                                        dcc.Link(
                                            "UCDP",
                                            href="https://ucdp.uu.se/downloads/index.html#candidate",
                                            target="_blank",
                                        ),
                                    ),
                                    html.Li(
                                        dcc.Link(
                                            "ACLED",
                                            href="https://acleddata.com",
                                            target="_blank",
                                        )
                                    ),
                                ]
                            ),
                        ],
                        title="About this App",
                        className="bg-opacity-10 me-5  ms-5  mt-3 border-light border-1 bg-light text-primary rounded",
                    ),
                ],
                start_collapsed=True,
            ),
        ]
    )
    return accordion
