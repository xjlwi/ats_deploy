import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

import os, math
import pandas as pd
from plotly import graph_objects as go
from pathlib import Path
dir = Path(__file__).parent
print (os.getcwd())
data_dir = os.path.join(os.getcwd(),'data/01_raw/ui/')
# os.chdir(dir)
#
Notion_db_content = 'https://www.notion.so/novalearn/b194bb2c04b1444084d1c3610d8bc672?v=0a63faf0c5074a9d9240e5a7f9c7a869&pvs=4'
n_signups = 44
sales_revenue = '$ 3000'
profit_ytd_val = '$ 80000'
weekly_rev = '$ 540'
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
# Radial shape components

def create_radial_component(planned_profit, target_profit):
    # Calculate the percentage of planned profit achieved
    percentage = (planned_profit / target_profit) * 100
    
    # Set the color of the radial shape based on the achievement percentage
    color = 'green' if percentage >= 100 else 'red'
    met = 'met' if percentage >= 100 else 'not met'
    # Calculate the circumference of the circle
    circumference = 2 * math.pi * 90
    
    # Calculate the dash length for the progress circle
    dash_length = (circumference / 100) * percentage
    
    # Create the inner HTML for the radial shape
    inner_html = f'''
        <svg height="200" width="200">
          <circle cx="100" cy="100" r="90" fill="#ffffff" stroke-width="10" stroke="#eaeaea" />
          <circle cx="100" cy="100" r="90" fill="transparent" stroke-width="10" stroke="{color}"
            stroke-dasharray="{dash_length},{circumference}" transform="rotate(-90 100 100)"/>
          <text x="50%" y="40%" text-anchor="middle" dominant-baseline="central" font-size="24">{percentage}%</text>
          <text x="50%" y="60%" text-anchor="middle" dominant-baseline="central" font-size="16">Target {met}</text>
        </svg>
    '''
    
    # Return the Dash component
    return html.Div([
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML(inner_html),
    ],
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
    )


def update_cards(Categoryoutput=None):
    Category = Categoryoutput
    print (Category)

    # Create the dbc.Graph figure for the second column
    layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=15, #right margin
                    b=19, #bottom margin
                    t=30  #top margin
                ),
            title = 'Sample number of view by month revenue',
            xaxis=dict(
                    showline=True,
                    linewidth=1,
                    linecolor='black'
                ),
            yaxis=dict(
                showline=True,
                linewidth=1,
                linecolor='black'
            ),
            plot_bgcolor='white',
            )
    dara = [go.Scatter(x=['Jan', 'Feb', 'Mar'], y=[4, 1, 2], mode='lines')]
    fig = dict(data=dara, layout=layout)
    
    
    # Create the dbc.Graph figure for the second column
    graph = dcc.Graph(
        figure=fig,
        style={'height': "200px", }
    )

    # Create the dbc.Graph figure for the html Radial chart
    planned_vs_kpi = html.Div([
        create_radial_component(2_000, 10_000)
    ])

    ## 
    if Category == 'Sales':
        # dynamic Card Content
        new_signups = dbc.Card([
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
        ], color = '#abdbe3', outline=True)

        # dynamic Sales
        new_sales = dbc.Card([
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
        ], color = '#abdbe3', outline=True)

        # dynamic Sales
        profit_ytd = dbc.Card([
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
        ], color = '#abdbe3', outline=True)

        # dynamic Sales
        weekly_revenue = dbc.Card([
                dbc.CardBody([
                html.H5("Weekly Revenue ", className="card-title",
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{weekly_rev}",
                    style={"text-align": "center",  # Set text alignment to center
                            "color": "white"} , # Set text alignment to center
                    className="card-text",
                ),
            ],
            id = "weekly_rev")
        ], color = '#abdbe3', outline=True)

        row_3 = dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([new_signups], className = "m-2"), 
                            dbc.Row([profit_ytd], className = "m-2"),
                            dbc.Row([new_sales], className = "m-2"),
                        ], 
                            width = 4),
                        # html.Div(style={'border-left': '5px solid #efededa1', 'height': '100%'}, className='verticalline'),
                        # dbc.Col([], width=1) #insert space,
                        dbc.Col([
                            dbc.Row([weekly_revenue],  className="m-2",), 
                            dbc.Row([graph],  style={'padding': '0'}), 
                                ],
                                width = 4),

                        dbc.Col([
                            dbc.Row([planned_vs_kpi], class_name = 'm-2',)
                        ],
                        width= 4),
                        # html.Hr(), html.Div(className="verticalline")
                        
                        # dbc.Col([], width=3),
                    ]
                ),
                # html.Div(
                #     id='chart-container',
                #     style={'padding': '0'}
                # ),
                html.Link(
                    rel='stylesheet',
                    href='/assets/custom.css'
                )
                # dbc.Row(
                #     [
                #         dbc.Col(html.Hr(), width = 4),
                #         dbc.Col(html.Div(className="verticalline"), width=6),
                #     ],
                #     id='HorizontalLine'
                # ),
                # dbc.Row(
                #     [
                #         # dbc.Col(dbc.Card(new_sales, color="#abdbe3", outline=True), width = 4),
                #         dbc.Col(html.Div(className="verticalline"), width=6),
                #     ]
                # ),
                # dbc.Row(
                #     [
                #         dbc.Col(html.Hr(), width = 4),
                #         dbc.Col(html.Div(className="verticalline"), width=6),
                #     ],
                #     id='HorizontalLine'
                # ),
                # dbc.Row(
                #     [
                #         # dbc.Col(dbc.Card(profit_ytd, color="#abdbe3", outline=True), width = 4),
                #         dbc.Col(html.Div(className="verticalline"), width=6),
                #     ],
                    
                # ),
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
                        # html.Hr(),  # horizontal line
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