import json

import dash
import dash_draggable
from dash import ALL, Input, Output, State, ctx, dcc, html

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
        self.app.layout = self.layout
        self.callbacks()

    def layout(self):
        layout, children = self.initialize_dashboard()
        return html.Div(
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
                        html.Div(id="output-text", style={"marginTop": "20px"}),
                    ],
                ),
                dash_draggable.GridLayout(
                    id="draggable-area",
                    children=children,
                    layout=layout,
                    save=False,
                    style={
                        "flex": "1",
                        "padding": "10px",
                        "backgroundColor": "black",
                    },
                ),
            ],
        )

    def initialize_dashboard(self):
        layout = []
        children = []
        layout_str = self.db.select_latest_layout()
        if not layout_str:
            return layout, children
        saved_layout = json.loads(layout_str)
        for id, pos in saved_layout.items():
            layout.append(pos)
            _, question, sql_query, plotly_code = self.db.select_one_visualisation(id)
            df = self.vanna.run_sql(sql_query)
            fig = self.vanna.get_plotly_figure(plotly_code, df)
            chart = chart_component(id, fig)
            children.append(chart)
        return layout, children

    def callbacks(self):
        @self.app.callback(
            Output("draggable-area", "layout", allow_duplicate=True),
            Input("draggable-area", "layout"),
            prevent_initial_call=True,
        )
        def save_layout(layout):
            map = {}
            for element in layout:
                map[element["i"]] = element
            layout_str = json.dumps(map)
            self.db.insert_layout(layout_str)
            return dash.no_update

        @self.app.callback(
            [
                Output("draggable-area", "children", allow_duplicate=True),
                Output("draggable-area", "layout", allow_duplicate=True),
            ],
            Input("submit-button", "n_clicks"),
            State("text-input", "value"),
            State("draggable-area", "children"),
            State("draggable-area", "layout"),
            prevent_initial_call=True,
        )
        def add_visualisation(n_clicks, query, current_children, current_layout):
            if not n_clicks or not query:
                return dash.no_update, dash.no_update

            sql = self.vanna.generate_sql(query)
            df = self.vanna.run_sql(sql)
            code = self.vanna.generate_plotly_code(
                query, sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}"
            )
            id = str(self.db.insert_visualisation(query, sql, code))
            fig = self.vanna.get_plotly_figure(code, df)
            new_child = chart_component(id, fig)

            new_x = 0
            new_y = 0
            if len(current_layout) > 0:
                for item in current_layout:
                    if new_y < item["y"] and new_x < item["x"]:
                        new_x = item["x"]
                        new_y = item["y"]
                if new_x + 3 > 12:
                    new_x = 0
                    new_y = new_y + 3
                else:
                    new_x = new_x + 3

            new_layout_item = {
                "i": id,
                "x": new_x,
                "y": new_y,
                "w": 3,
                "h": 3,
            }

            updated_children = current_children + [new_child]
            updated_layout = current_layout + [new_layout_item]

            return updated_children, updated_layout

        @self.app.callback(
            [
                Output("draggable-area", "children", allow_duplicate=True),
                Output("draggable-area", "layout", allow_duplicate=True),
            ],
            Input({"type": "delete-chart-button", "index": ALL}, "n_clicks"),
            State("draggable-area", "children"),
            State("draggable-area", "layout"),
            prevent_initial_call=True,
        )
        def delete_chart(_, current_children, current_layout):
            if not ctx.triggered_id or not ctx.triggered[0]["value"]:
                return dash.no_update, dash.no_update

            if ctx.triggered_id["type"] != "delete-chart-button":
                return dash.no_update, dash.no_update

            chart_id = ctx.triggered_id["index"]

            self.db.delete_one_visualisation(chart_id)

            updated_children = [
                child for child in current_children if child["props"]["id"] != chart_id
            ]
            updated_layout = [
                child for child in current_layout if child["i"] != chart_id
            ]

            return updated_children, updated_layout

    def start(self):
        self.app.run_server(host="0.0.0.0", port=Environment.PORT)


def chart_component(id: str, fig):
    button = html.Button(
        "X",
        id={
            "type": "delete-chart-button",
            "index": id,
        },
        style={
            "width": "100%",
        },
    )
    chart = dcc.Graph(
        responsive=True,
        figure=fig,
        style={
            "min-height": "0",
            "flex-grow": "1",
        },
    )
    return html.Div(
        children=[
            button,
            chart,
        ],
        id=id,
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
