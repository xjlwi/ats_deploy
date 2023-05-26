import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

#################################################################
#                   COMPONENETS                                 #
#################################################################

def update_cards(Category=None):
    if isinstance(Category, str):
            # dynamic Card Content
            card_content = [
                dbc.CardHeader("Card header"),
                dbc.CardBody([
                    html.H5("Card title", className="card-title"),
                    html.P(
                        f"{Category}",
                        className="card-text",
                    ),
                ],
                id = "card-content")
            ]
            row_3 = dbc.Row(
                [
                    dbc.Col(dbc.Card(card_content, color="success", outline=True)),
                    dbc.Col(dbc.Card(card_content, color="dark", outline=True)),
                ],
                id='CardRow'
            )
            return row_3
    else:
        Category = 'This is the default text for Cards.'
        # Card Content
        card_content = [
            dbc.CardHeader("Card header"),
            dbc.CardBody([
                html.H5("Card title", className="card-title"),
                html.P(
                    f"{Category}",
                    className="card-text",
                ),
            ],
            id = "card-content")
        ]
        row_3 = dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="success", outline=True)),
                dbc.Col(dbc.Card(card_content, color="dark", outline=True)),
            ],
            id='CardRow'
        )
        return row_3


select_menu = dbc.Row(
    [
        html.Div([
                html.Div([
                    dcc.Dropdown(
                    ['Operations', 'Events', 'Product', 'Creative & Courses', 'Marketing', 'Sales'], 
                    # 'Operations',
                    id = 'Category',         
                    style={'color': '#1B053B', 'background-color': '#1CB0F6'} )
                ])
            ],
                style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]
)
    

product_menu = dbc.Row([
    html.Div([
            dcc.Dropdown(
                ['NovaHome', 'NovaClass', 'NovaSchool', 'NovaTech'],
                'NovaHome',
                id='product_category',
                style={'color': '#1B053B', 'background-color': '#1CB0F6',} 
            ),
            html.Br(),
        ],
        style={'width': '50%', 'display': 'inline-block'}),
])


row_3 = update_cards()


#################################################################
#                           LAYOUT                              #
#################################################################
def layout_home():
    return html.Div(
        children=[
            html.H1("Home Page"),
            html.P("Welcome to the Home Page!"),
            row_3,
            html.Br(),
            select_menu,
        ]
            
    )

def layout_operation():
    return html.Div(
        children=[
            html.H1("👩🏻‍💼 Operation Page"),
            html.P("Welcome to the Novalearn Operations Page!"),
            row_3,
            html.Br(),
            select_menu,
        ]
            
    )


def layout_creative():
    return html.Div(
        children=[
            html.H1("🎨 Creative and Content Page"),
            html.P("Welcome to the Novalearn Creative Page!"),
            html.Br(),
        ]
            
    )

def layout_product():
    return html.Div(
        children=[
            html.H1("🌐 Product Page"),
            html.P("Welcome to the Product Page!"),
            html.Br(),
            product_menu,
            html.Div([
                dcc.Graph(id='GraphProduct'),
            ],
            style={'width': '50%', 'display': 'inline-block'}),

        ],
        id="PRODUCT_PAGE",
    )