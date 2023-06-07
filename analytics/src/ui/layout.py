import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import os
import pandas as pd
from pathlib import Path
dir = Path(__file__).parent
# print (os.getcwd())
data_dir = os.path.join(os.getcwd(),'data/01_raw/ui/')
# os.chdir(dir)

#################################################################
#                   DATA LOADING                                #
#################################################################
data = pd.read_csv(f'{data_dir}Sample Status.csv')
print(data.head())

# sort by remove Tags
data.columns = [x.lower().strip() for x in data.columns]
data = data.drop(columns=['id', 'tags'])
      

#################################################################
#                   COMPONENETS                                 #
#################################################################

def update_cards(Category=None):
    if isinstance(Category, str):
            # dynamic Card Content
            card_content = [
                dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("KPI🏆", className="card-title"),
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
    else: # DEFAULT CARDS
        Category = 'This is the default text for Cards.'
        # Card Content
        card_content = [
            dbc.CardHeader("Card header"),
            dbc.CardBody([
                html.H5("KPI🏆", className="card-title"),
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
                    style={'color': '#1B053B', 'background-color': '#1CB0F6', 'textAlign':'center'} )
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
                style={'color': '#1B053B', 'background-color': '#1CB0F6', 'textAlign':'center'} 
            ),
            html.Br(),
        ],
        style={'width': '50%', 'display': 'inline-block'}),
])

n_works = print(len(data.title.unique()))

row_3 = update_cards()

# List of ongoing Events
    ### UPCOMING EVENTS ###
events= dbc.Row(
            [   
                ## Upcoming events
                dbc.Col(
                    [
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Upcoming Event 1"),
                                dbc.DropdownMenuItem("Upcoming Event 2"),
                                dbc.DropdownMenuItem("Upcoming Event 3"),
                            ],
                            label="Upcoming Events",
                        )
                    ],
                    width=6,  # Adjust the width of the column as needed
                ),
                ## Ongoing events
                dbc.Col(
                    [
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Ongoing Event 1"),
                                dbc.DropdownMenuItem("Ongoing Event 2"),
                                dbc.DropdownMenuItem("Ongoing Event 3"),
                            ],
                            label="Ongoing Events",
                        )
                    ],
                    width=6,  # Adjust the width of the column as needed
                ),
            ]

            
        )


    ### ONGOING EVENTS ###
#     dbc.DropdownMenu(
#         [
#             dbc.DropdownMenuItem(
#             dbc.Row(
#                 [
#                 dbc.Col(
#                     [
#                         html.Ul(
#                             [
#                                 html.Li("Ongoing A"),
#                                 html.Li("Ongoing B"),
#                                 html.Li("Ongoing C"),
#                             ]
#                         ),
#                     ],
#                     width=6,  # Adjust the width of the column as needed
#                     ),
#                 ]
#                 )
#             ),
#         ],
#         label="ONGOING EVENTS",
#         nav=True,
#         in_navbar=True,
#         color='info',
#     )
#     ],
#     fluid=True,
# )
                        # dbc.Col(
                        #     [
                        #         html.H4("Post-Events"),
                        #         html.Ul(
                        #             [
                        #                 html.Li("Claims"),
                        #                 html.Li("Post-Event Sales"),
                        #                 html.Li("Item C"),
                        #             ]
                        #         ),
                        #     ],
                        #     width=4,  # Adjust the width of the column as needed
                        #  ),
                        
  

    

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
            ## LIST OF PROGRAMS ##
            # html.Div([
            #     html.H4("Upcoming Events"),
            #     html.Li("Events Upcoming"),
            #     html.H4("Ongoing Events"),
            #     html.Li([
            #          html.P("ASA ISNS"),
            #     ]),
            # ]),
            events,
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
            html.H1("🌐 Product Page 🐱‍💻"),
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