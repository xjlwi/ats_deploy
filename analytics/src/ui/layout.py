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
#
Notion_db_content = 'https://www.notion.so/novalearn/b194bb2c04b1444084d1c3610d8bc672?v=0a63faf0c5074a9d9240e5a7f9c7a869&pvs=4'
n_signups = 44
sales_revenue = '$ 3000'
profit_ytd_val = '$ 80000'
#################################################################
#                   DATA LOADING                                #
#################################################################
# data = pd.read_csv(f'{data_dir}Sample Status.csv')
# print(data.head())

# # sort by remove Tags
# data.columns = [x.lower().strip() for x in data.columns]
# data = data.drop(columns=['id', 'tags'])
      

#################################################################
#                   COMPONENETS                                 #
#################################################################

def update_cards(Categoryoutput=None):
    Category = Categoryoutput
    print (Category)
    if Category == 'Sales':
        # dynamic Card Content
        new_signups = [
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H5("New Signups", className="card-title", 
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{n_signups} ",
                    style={"text-align": "center",
                            "color": "white"}, # Set text alignment to center
                    className="card-text",
                ),
            ],
            id = "new_signups")
        ]

        # dynamic Sales
        new_sales = [
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H5("New Sales Revenue", className="card-title",
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{sales_revenue}",
                    style={"text-align": "center",  # Set text alignment to center
                            "color": "white"} ,  # Set font color to white # Set text alignment to center
                    className="card-text",
                ),
            ],
            id = "new_sales_revenue")
        ]

        # dynamic Sales
        profit_ytd = [
                dbc.CardBody([
                html.H5("Profit YTD ", className="card-title",
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{profit_ytd_val}",
                    style={"text-align": "center",  # Set text alignment to center
                            "color": "white"} , # Set text alignment to center
                    className="card-text",
                ),
            ],
            id = "proft_ytd")
        ]
        row_3 = html.Div(
                [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(new_signups, color="#abdbe3", outline=True), width = 4),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Hr(), width = 4),
                    ],
                    id='HorizontalLine'
                ),
                dbc.Row(
                    [
                    dbc.Col(dbc.Card(new_sales, color="#abdbe3", outline=True), width = 4),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Hr(), width = 4),
                    ],
                    id='HorizontalLine'
                ),
                dbc.Row(
                    [
                    dbc.Col(dbc.Card(profit_ytd, color="#abdbe3", outline=True), width = 4),
                    ],
                    
                ),
                html.Div(className="vertical-line"),
                ],
                id='CardRow'
        )
        
        return row_3
    else: # DEFAULT CARDS
        content = f'This is the default text for {Category}.'
        # Card Content
        card_content = [
            # dbc.CardHeader("Card header"),
            dbc.CardBody([
                html.H5("KPI🏆", className="card-title",
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{content}",
                    className="card-text",
                    style={"text-align": "center",  # Set text alignment to center
                            "color": "white"} ,
                ),
            ],
            id = "card-content")
        ]
        row_3 = html.Div(
                [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content, color="#abdbe3", outline=True), width = 4),
                    ],
                    id='KPI'
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Hr(), width = 4),
                    ],
                    id='HorizontalLine'
                ),
                dbc.Row(
                    [
                    dbc.Col(dbc.Card(card_content, color="#abdbe3", outline=True), width = 4),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Hr(), width = 4),
                    ],
                    id='HorizontalLine'
                ),
                dbc.Row(
                    [
                    dbc.Col(dbc.Card(card_content, color="#abdbe3", outline=True), width = 4),
                    ]
                ),
                html.Div(className="vertical-line"),
                ],
                id = 'CardRow'
        )
        return row_3


# select_menu = dbc.Row(
#     [
#         html.Div([
#                 html.Div([
#                     dcc.Dropdown(
#                     options = [ {"label": "Operations", "value": "Operations"},
#                                 {"label": "Events", "value": "Events"},
#                                 {"label": "Product", "value": "Product"},
#                                 {"label": "Creative & Courses", "value": "Creative & Courses"},
#                                 {"label": "Marketing", "value": "Marketing"},
#                                 {"label": "Sales", "value": "Sales"},], 
#                     id='Category',         
#                     style={ 'textAlign':'center'} )
#                 ])
#             ],
#                 ) #style={'width': '40%', 'float': 'right', 'display': 'inline-block'}
#     ]
# )
    
select_menu = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Pick a Category"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Category", width=2),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="Category",
                                        options=[
                                            {"label": "Operations", "value": "Operations"},
                                            {"label": "Events", "value": "Events"},
                                            {"label": "Product", "value": "Product"},
                                            {"label": "Creative & Courses", "value": "Creative & Courses"},
                                            {"label": "Marketing", "value": "Marketing"},
                                            {"label": "Sales", "value": "Sales"},
                                        ],
                                        value="Sales", # set default to Sales
                                    ),
                                    width=10
                                ),
                            ]
                        ),
                        html.Hr(),  # horizontal line
                        html.Div(id="Categoryoutput"),
                    ]
                ),
            ]
        ),
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
            # html.H1("Home Page"),
            html.P("Welcome to the Home Page!"),
            select_menu,
            html.Br(),
            row_3,
            # select_menu,
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