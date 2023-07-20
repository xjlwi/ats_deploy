#@source: https://github.com/zoltanmaric/coppersushi/blob/main/app.py 

import os
import pathlib
import re

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# get relative data folder
PATH = pathlib.Path(__file__).parent

from layout import (
    layout_creative,
    layout_home,
    layout_product, 
    layout_operation,
    update_cards,
    update_courses_tracker,
    courses_raw,
    # progress_bar,
    update_progress_bar
)

app = dash.Dash(__name__, title='Novalearn Internal Dashboard 🍣', external_stylesheets=[dbc.themes.FLATLY, "assets/custom.css"])
app.config["suppress_callback_exceptions"] = True

server = app.server

# Load data
# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# CSS styles


app.layout =  dbc.Container([

    #################################################
    #               MULTI-PAGE                      #
    #################################################
    dcc.Location(id="url", refresh=False),
        html.Nav(
            children=[
                html.A("Home", href="/", className="nav-link"),
                html.A("Product", href="/product", className="nav-link"),
                html.A("Marketing", href="/marketing", className="nav-link"),
                html.A("Creative", href="/creative", className="nav-link"),
            ],
            className="navbar"
        ),
        html.Div(id="page-content")
], fluid=True)

# @app.callback(
#     Output('indicator-graphic', 'figure'),
#     Input('xaxis-column', 'value'),
#     Input('yaxis-column', 'value'),
#     Input('Category', 'value'),
#     Input('product_category', 'value'),
#     Input('year--slider', 'value'))
# def update_graph(Category, product_category,
#                  year_value):
#     dff = df[df['Year'] == year_value]
#     fig = go.Figure()
#     # fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#     #                  y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#     #                  hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

#     # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

#     # fig.update_xaxes(title=Category,
#     #                  )

#     # fig.update_yaxes(title=product_category,
#     #                 )
#     fig.update_layout(title = Category)

#     return fig


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/product":
        return layout_product()
    elif pathname == "/creative":
        return layout_creative()
    elif pathname == "/marketing":
        return layout_operation()
    else:
        return layout_home()

@app.callback(Output("GraphProduct", 'figure'), [Input("product_category", "value")])
def update_graph_product(product_category):
    print(product_category)
    if product_category == 'NovaClass':
        return go.Figure(data=go.Bar(x=['A','B','C'], y =[10, 20, 30]))
    else:
        # Generate default graph
        return go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 1, 2], mode="lines"))

@app.callback(Output("CardRow", 'children'), [Input('Category',"value")])
def update_cards_heading(Category):
    return update_cards(Category)
    
@app.callback(Output ("CoursesTracker", 'figure'), [Input('monthRange', 'value')])
def update_courses_charts(monthRange):
    return update_courses_tracker(courses_raw, monthRange)

# Create a callback to update the progress bar
@app.callback(
    Output ("ProgressBar", "children"), ## TODO
    [Input('my-button', 'n_clicks')]
)
def update_progress(n_clicks):
    return update_progress_bar(n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)