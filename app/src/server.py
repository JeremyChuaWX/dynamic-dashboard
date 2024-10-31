import dash
import dash_draggable
import pandas as pd
import plotly.express as px
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State

from environment import Environment

APP_NAME = "Dynamic Dashboard"
EXTERNAL_STYLESHEETS = ["./style.css"]

app = dash.Dash(APP_NAME, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "row",
        "minHeight": "100vh",  # Ensure the whole screen is used
        "backgroundColor": "black",
        "color": "white",
    },
    children=[
        # Sidebar: Chart panel
        html.Div(
            style={
                "flex": "0 0 20%",  # Fixed 20% width for the sidebar
                "padding": "10px",
                "borderRight": "1px solid white",
                "overflowY": "auto",
                "backgroundColor": "#222",
            },
            children=[
                html.H3("Chart Panel", style={"textAlign": "center"}),
                html.Div(
                    "Click charts to add/remove from the main area",
                    style={"marginBottom": "10px"},
                ),
                # Input box for queries
                dcc.Input(
                    id="text-input",
                    type="text",
                    placeholder="Enter your query...",
                    style={"width": "100%", "marginBottom": "10px"},
                ),
                # Sidebar clickable items
                html.Div(
                    id="chart-store",
                    children=[
                        html.Button(
                            "Scatter Plot",
                            id="scatter-item",
                            className="draggable-item",
                            n_clicks=0,
                        ),
                        html.Button(
                            "Bar Chart",
                            id="bar-item",
                            className="draggable-item",
                            n_clicks=0,
                        ),
                        html.Button(
                            "Line Chart",
                            id="line-item",
                            className="draggable-item",
                            n_clicks=0,
                        ),
                    ],
                ),
            ],
        ),
        # Main area: Displays selected charts
        dash_draggable.ResponsiveGridLayout(
            id="draggable-area",
            layouts={"lg": []},  # Start with an empty layout
            children=[],
            style={
                "flex": "1",  # Take up remaining space
                "padding": "10px",
                "backgroundColor": "black",
            },
        ),
    ],
)


# Callback to add/remove charts on click
@app.callback(
    Output("draggable-area", "children"),
    [Input(chart_id, "n_clicks") for chart_id in CHARTS.keys()],
    State("draggable-area", "children"),
)
def update_charts(*args):
    # Get which button was clicked
    ctx = callback_context

    # Current state of the charts on the main page
    current_children = list(args[-1])

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Get chart details from CHARTS dict
    chart_info = CHARTS[button_id]
    graph_id = chart_info["graph_id"]

    # Check if the graph is already displayed
    graph_exists = any(child["props"]["id"] == graph_id for child in current_children)

    if graph_exists:
        # If the chart is already on the page, remove it
        current_children = [
            child for child in current_children if child["props"]["id"] != graph_id
        ]
    else:
        # If not, add the chart to the page
        current_children.append(
            dcc.Graph(id=graph_id, figure=chart_info["figure"], responsive=True)
        )

    return current_children


# Callback to handle input submission
@app.callback(Output("text-input", "value"), Input("text-input", "value"))
def handle_query(input_value):
    if input_value:
        print(f"User Query: {input_value}")  # This is where you can handle the input
    return dash.no_update


def main():
    app.run_server(debug=True, port=Environment.PORT)
