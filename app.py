import pandas as pd
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
    use_pages=True,
    pages_folder="pages",
    suppress_callback_exceptions=True,
)


########### Navbar design section####################
# dropdown w/ quick links to navigate to the other pages
quickLinksLabels = {
    "Home": "Home",
    "World": "World",
    "Countries": "Countries",
    "Conflictsindex": "Conflictsindex",
    # "Watchlist": "Watchlist",
}

nav = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(quickLinksLabels[page["name"]], href=page["path"])
        for page in dash.page_registry.values()
        if (page["module"] != "pages.not_found_404") & (page["name"] != "Internal")
    ],
    nav=True,
    in_navbar=True,
    label="Quick Links",
    className="me-5 text-primary fw-bold ",
)
# assembly the navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=dash.get_asset_url("LOGO.png"),
                                    height="30px",
                                ),
                            ],
                            className="me-2",
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "World Crisis Discovery Report - 2024 Jan-May",
                                className="ms-2 text-primary fw-bold",
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
            ),
            nav,
        ]
    ),
    dark=True,
    className="p-2 fw-bold rounded",
)

# page container
content = html.Div(id="page-content", children=[page_container], className="content")

# main app layout
app.layout = dbc.Container(
    [dbc.Row([dbc.Col([navbar, content], width=12)])],
    fluid=False,
    style={},
    className="bg-opacity-20 p-2 bg-light rounded border border-light mh-100",
)


if __name__ == "__main__":
    app.run_server(debug=True)  # , dev_tools_ui=False, dev_tools_props_check=False)
