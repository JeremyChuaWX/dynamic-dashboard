import json

import dash
import dash_draggable
from dash import dcc, html
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
        layout, children = self.load_dashboard()
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
                            style={
                                "width": "100%",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Button(
                            "Submit",
                            id="submit-button",
                            style={
                                "width": "100%",
                            },
                        ),
                        html.Button(
                            "Save Layout",
                            id="save-layout-button",
                            style={
                                "width": "100%",
                                "marginTop": "10px",
                            },
                        ),
                        html.Div(id="output-text", style={"marginTop": "20px"}),
                    ],
                ),
                dash_draggable.GridLayout(
                    id="draggable-area",
                    layout=layout,
                    children=children,
                    style={
                        "flex": "1",
                        "padding": "10px",
                        "backgroundColor": "black",
                    },
                ),
            ],
        )

    def load_dashboard(self):
        print("loading dashboard ...")
        layout = []
        children = []
        layout_str = self.db.select_latest_layout()
        if not layout_str:
            return (layout, children)
        saved_layout = json.loads(layout_str)
        for id, pos in saved_layout.items():
            layout.append(pos)
            _, question, sql_query, plotly_code = self.db.select_one_visualisation(id)
            df = self.vanna.run_sql(sql_query)
            fig = self.vanna.get_plotly_figure(plotly_code, df)
            chart = dcc.Graph(
                id=id,
                figure=fig,
                style={
                    "marginBottom": "20px",
                },
            )
            children.append(
                html.Div(
                    chart,
                    key=id,
                    style={
                        "backgroundColor": "#333",
                        "padding": "10px",
                    },
                )
            )
        return (layout, children)

    def callbacks(self):
        @self.app.callback(
            Input("save-layout-button", "n_clicks"),
            Input("draggable-area", "layout"),
            State("draggable-area", "children"),
        )
        def save_layout(n_clicks, layout, children):
            if not n_clicks:
                return dash.no_update
            map = {}
            for position, child in zip(layout, children):
                map[child["props"]["key"]] = position
            layout_str = json.dumps(map)
            self.db.insert_layout(layout_str)

        @self.app.callback(
            Output("draggable-area", "children"),
            Input("submit-button", "n_clicks"),
            State("text-input", "value"),
            State("draggable-area", "children"),
        )
        def add_visualisation(n_clicks, query, current_children):
            if not n_clicks or not query:
                return current_children
            sql = self.vanna.generate_sql(query)
            df = self.vanna.run_sql(sql)
            code = self.vanna.generate_plotly_code(
                query, sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}"
            )
            id = str(self.db.insert_visualisation(query, sql, code))
            fig = self.vanna.get_plotly_figure(code, df)
            chart = dcc.Graph(
                id=id,
                responsive=True,
                figure=fig,
                style={
                    "min-height": "0",
                    "flex-grow": "1",
                },
            )
            current_children.append(
                html.Div(
                    chart,
                    key=id,
                    style={
                        "height": "100%",
                        "width": "100%",
                        "display": "flex",
                        "flex-direction": "column",
                        "flex-grow": "0",
                        "backgroundColor": "#333",
                        "padding": "10px",
                    },
                )
            )
            return current_children

    def start(self):
        self.app.run_server(host="0.0.0.0", port=Environment.PORT)
