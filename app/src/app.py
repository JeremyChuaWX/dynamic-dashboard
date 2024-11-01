import dash
import dash_draggable
import pandas as pd
import plotly.express as px
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State

from database import Database
from environment import Environment
from llm import Vanna

APP_NAME = "Dynamic Dashboard"
EXTERNAL_STYLESHEETS = ["./style.css"]


class App:
    def __init__(self, vanna: Vanna, db: Database) -> None:
        self.vanna = vanna
        self.db = db
        self.app = dash.Dash(APP_NAME, external_stylesheets=EXTERNAL_STYLESHEETS)
        self.layout()
        self.callbacks()

    def layout(self):
        self.app.layout = html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "minHeight": "100vh",
                "backgroundColor": "black",
                "color": "white",
            },
            children=[
                html.Div(
                    style={
                        "flex": "0 0 20%",
                        "padding": "10px",
                        "borderRight": "1px solid white",
                        "overflowY": "auto",
                        "backgroundColor": "#222",
                    },
                    children=[
                        html.H3("Chat", style={"textAlign": "center"}),
                        dcc.Input(
                            id="text-input",
                            type="text",
                            placeholder="Enter your query...",
                            style={"width": "100%", "marginBottom": "10px"},
                        ),
                        html.Button(
                            "Submit", id="submit-button", style={"width": "100%"}
                        ),
                        html.Div(id="output-text", style={"marginTop": "20px"}),
                    ],
                ),
                dash_draggable.ResponsiveGridLayout(
                    id="draggable-area",
                    layouts={"lg": []},
                    children=[],
                    style={
                        "flex": "1",
                        "padding": "10px",
                        "backgroundColor": "black",
                    },
                ),
            ],
        )

    def callbacks(self):
        @self.app.callback(
            Output("draggable-area", "children"),
            Input("submit-button", "n_clicks"),
            State("text-input", "value"),
            State("draggable-area", "children"),
        )
        def update_dashboard(n_clicks, query, current_children):
            if not n_clicks or not query:
                return current_children

            sql = self.vanna.generate_sql(query)
            df = self.vanna.run_sql(sql)
            code = self.vanna.generate_plotly_code(
                query, sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}"
            )
            fig = self.vanna.get_plotly_figure(code, df)
            chart = dcc.Graph(
                id=f"chart-{n_clicks}",
                figure=fig,
                style={"marginBottom": "20px"},
            )
            current_children.append(
                html.Div(
                    chart,
                    key=f"chart-{n_clicks}",
                    style={"backgroundColor": "#333", "padding": "10px"},
                )
            )

            return current_children

    def start(self):
        self.app.run_server(host="0.0.0.0", port=Environment.PORT)
