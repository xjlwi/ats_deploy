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
b2b_sales = '$ 3000'
b2c_sales = '$ 800'
weekly_rev = '$ 540'

avg_revenue_per_course = '$ 20'
number_of_active_users = '60'
number_of_events_ytd = 10

opex_value = '$20 000'
capex_value = '$5 000'

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

# Opex + Capex (With Icons indicators)
def create_opex_card():
   opex_card =  dbc.Card(
    dbc.CardBody(
        [
            # First row
            dbc.Row(
            children=[
                dbc.Col(
                        html.Img(src="assets/Opex.png", className="rounded-img", style={"height": "100px", "width": "100px"}),
                        width=3, 
                        ),
                dbc.Col(
                    html.P("80 000", className="card-text-header1"),
                    width=6
                ),
            ], 
            align = "center"
            ),
            
            # Second row
            dbc.Row(
                [
                    html.Br(),
                    html.Div(className="opex-cost", style={"marginLeft": "auto"}, 
                             children= [
                                        html.P("OPEX HKD", className='card-text-header2',)
                                    ],
                ),
                ], 
            align = "center"
            ),
        ]
    ),          
    className="cards-grey",
    )

   capex_card = dbc.Card(
        dbc.CardBody(
        [
            # First row
            dbc.Row(
            # style={"backgroundColor": "#121211a1", "borderRadius": "8px", "padding": "16px"},
            children=[
                dbc.Col(
                        html.Img(src="assets/Capex.png", className="rounded-img", style={"height": "100px", "width": "100px"}),
                        width=2
                        ),
                dbc.Col(
                    html.P("12 000", className="card-text-header1"),
                    width= 9
                ),
            ], 
            align = "center"
            ),
            
            # Second row
            dbc.Row(
                [
                    html.Div(className="capex-cost", style={"marginLeft": "auto"}, 
                             children= [
                                        html.P("CAPEX HKD", className='card-text-header2')
                                    ],
                ),
                ], 
            align = "center"
            ),
        ]
    ),          
    className="cards-grey",
    )

    ## Structure layout of cards
   
   # Add a Container object to position the cards
   CARDS = dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([capex_card],  className="m-2",), 
                            ], 
                            width = 6),
                        dbc.Col([
                            dbc.Row([opex_card], className="m-2"),
                                ],
                                width = 6),
                            ]),
                        ],
                id='opex_capex_row'
        )
   
   return CARDS

# Opex + Capex
def get_opex_capex():
     
    opex_card = dbc.Card([
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H3("OPEX", className="card-title", 
                        style={"text-align": "center",  # Set text alignment to center
                                "color": "white"} ,),
                html.P(
                    f"{opex_value} ",
                    style={"text-align": "center",
                            "color": "white"}, # Set text alignment to center
                    className="card-text",
                ),
            ],
            id = "opex_cards")
        ], color = '#73edc6a1', outline=True)
        # ], color = '#abdbe3', outline=True)
     
    capex_card = dbc.Card([
        # dbc.CardHeader(f"{Category.upper()}"),
        dbc.CardBody([
            html.H3("CAPEX", className="card-title", 
                    style={"text-align": "center",  # Set text alignment to center
                            "color": "white"} ,),
            html.P(
                f"{capex_value} ",
                style={"text-align": "center",
                        "color": "white"}, # Set text alignment to center
                className="card-text",
            ),
        ],
        id = "capex_cards")
        ], color = '#73edc6a1', outline=True)
    
    opex_capex_outline = dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([opex_card], className="m-2"),
                            ], 
                            width = 6),
                        dbc.Col([
                            dbc.Row([capex_card],  className="m-2",), 
                                ],
                                width = 6),
                            ]),
                        ],
                id='opex_capex_row'
        )
    return opex_capex_outline


# Sidebar
# Define the sidebar layout
def create_sidebar():
    sidebar = html.Div(
        id='sidebar',
        children=[
            # html.H2('Sidebar')
        
            html.Button(
                html.Img(src='assets/sidebar/gauge-chart.png', height='20px', width='20px'),
                id='btn-layout-1', n_clicks=0
            ),
            html.Button(
                html.Img(src='assets/sidebar/people.png', height='20px', width='20px'),
                id='btn-layout-2', n_clicks=0
            ),
            html.Button(
                html.Img(src='assets/sidebar/briefcase.png', height='20px', width='20px'),
                id='btn-layout-3', n_clicks=0
            )
        ],
        className='sidebar'
    )

    return sidebar
# Reference the Category, Return the Sales Page 3 rows of layout.
def update_cards(Categoryoutput=None):
    Category = Categoryoutput
    Category = 'Sales' # Set to default for now.
    print (Category)

    # Create the dbc.Graph figure for the second column
    layout = go.Layout(
            margin=go.layout.Margin(
                    l=20, #left margin
                    r=30, #right margin
                    b=30, #bottom margin
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
            font=dict(
                size=9,
            ),
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
                html.H5("New Signups", className="card-text-header2", 
                        # style={"text-align": "center",  # Set text alignment to center
                        #         "color": "white"} ,
                        ),
                html.P(
                    f"{n_signups} ",
                    # style={"text-align": "center",
                    #         "color": "white"}, # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "new_signups")
        ], className="capex-card")

        # dynamic Sales
        new_sales = dbc.Card([
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H5("New Sales Revenue", className="card-text-header2",
                        # style={"text-align": "center",  # Set text alignment to center
                        #         "color": "white"} ,),
                    ),
                html.P(
                    f"{b2b_sales}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} ,  # Set font color to white # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "new_sales_revenue")
        ], className="capex-card")

        # dynamic Sales
        profit_ytd = dbc.Card([
                dbc.CardBody([
                html.H5("B2C Sales ", className="card-text-header2",
                        # style={"text-align": "center",  # Set text alignment to center
                        #         "color": "white"} ,
                ),
                html.P(
                    f"{b2c_sales}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "proft_ytd")
        ], className="capex-card")

        # dynamic Sales
        weekly_revenue = dbc.Card([
                dbc.CardBody([
                html.H5("B2B Sales", className="card-text-header2"),
                html.P(
                    f"{weekly_rev}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "weekly_rev")
        ], className="capex-card")

        row_3 = dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([weekly_revenue],  className="m-2",), 
                            dbc.Row([profit_ytd], className = "m-2"),
                            dbc.Row([new_sales], className = "m-2"),
                        ], 
                            width = 4),
                        # html.Div(style={'border-left': '5px solid #efededa1', 'height': '100%'}, className='verticalline'),
                        # dbc.Col([], width=1) #insert space,
                        dbc.Col([
                            dbc.Row([new_signups], className = "m-2"), 
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
                ],
                id='CardRow'
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


events = dbc.Container([
                dbc.Row([
                    ## Upcoming events
                    dbc.Col([
                        html.Br(),
                        dbc.DropdownMenu(
                                [
                                    dbc.DropdownMenuItem("Upcoming Event 1"),
                                    dbc.DropdownMenuItem("Upcoming Event 2"),
                                    dbc.DropdownMenuItem("Upcoming Event 3"),
                                ],
                                label="Upcoming Events",
                            )
                    ],
                    width={"size": 3, "offset": 1},  
                    ),
                    ## Ongoing events
                    dbc.Col([
                        html.Br(),
                        dbc.DropdownMenu(
                                [
                                    dbc.DropdownMenuItem("Ongoing Event 1"),
                                    dbc.DropdownMenuItem("Ongoing Event 2"),
                                    dbc.DropdownMenuItem("Ongoing Event 3"),
                                ],
                                label="Ongoing Events",
                            )
                        ],
                        width={"size": 3, "offset": 3},  
                    ),
                ])
],id='emptyRow')

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
                            ],
                            class_name = 'm-2'
                        ),
                        # html.Hr(),  # horizontal line
                        html.Div(id="Categoryoutput"),
                        html.Br()
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

# Create the function to return the html layout contents
row_3 = update_cards()
opex_capex = get_opex_capex()



########################################################
#              COMPONENTS OPERATIONS BOTTOM            #
########################################################
layout = go.Layout(
            margin=go.layout.Margin(
                    l=10, #left margin
                    r=15, #right margin
                    b=19, #bottom margin
                    t=30  #top margin
                ),
            title = 'Area Line Chart',
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
temp = go.Figure(data=[
    go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[3, 2, 4, 1, 2],
        fill="tozeroy",
        mode="lines",
        marker=dict(color="#abd9e3", line=dict(color="#abdbe3")),
        fillcolor="#abdbe3",  # Set the fill color
        )
    ],
    layout=layout
)
# Create the dbc.Graph figure for the second column
graph = dcc.Graph(
    figure=temp,
    style={'height': "100px", }
)

def get_target_revenue():
    # 3 rows, 2 columns. Each row: Card LHS || Area Chart RHS

    ## CARDS : 3 samples (avg revenue per course, number of active users, # of events YTD)
    avg_revenue_card = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("Average Revenue / course $", className="card-text-header2"), 
                    html.P(
                        f"{avg_revenue_per_course} ",
                        # style={"text-align": "center",
                        #         "color": "white"}, # Set text alignment to center
                        className="card-text-body2",
                    ),
                ],
                id = "new_signups")
            ], className="sales-card")

    n_active_card = dbc.Card([
                dbc.CardBody([
                    html.H5("# of Active Users", className="card-text-header2"), 
                            # style={"text-align": "center",  # Set text alignment to center
                            #         "color": "white"} ,),
                    html.P(
                        f"{str(number_of_active_users)} ",
                        # style={"text-align": "center",
                        #         "color": "white"}, # Set text alignment to center
                        className="card-text-body2",
                    ),
                ],
                id = "new_signups")
            ], className="sales-card")

    events_ytd_card = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("# Events YTD", className="card-text-header2"), 
                            # style={"text-align": "center",  # Set text alignment to center
                            #         "color": "white"} ,),
                    html.P(
                        f"{number_of_events_ytd} ",
                        # style={"text-align": "center",
                        #         "color": "white"}, # Set text alignment to center
                        className="card-text-body2",
                    ),
                ],
                id = "new_signups")
            ], className="sales-card")

    ##########################################################
    #       Chart the 3 rows, LHS Card, RHS Graph            #
    ##########################################################
    target_revenue = dbc.Container([
                        ### HEADER ROW ###
                        dbc.Row(
                            dbc.Col(
                                    html.H2("Sales by Business", className='page-header'),
                                    # width={"size": 12, "align":'stretch', "color":'#fffbfb'},
                            ),
                            justify='center',
                        ),

                        ### FIRST ROW ###
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([avg_revenue_card], 
                                        className = "m-2", 
                                        style={'padding': '0'}, ), 
                                # dbc.Row([graph],  style={'padding': '0'}), 
                            ], 
                                width = 4),
                            dbc.Col([
                                dbc.Row([graph],  style={'padding': '0'}), 
                            ],
                                    width = 8),

                        ]
                    ),

                    ### SECOND ROW ###
                    dbc.Row([
                            dbc.Col([
                                dbc.Row([n_active_card], className = "m-2", 
                                        style={'padding': '0'}, ),
                            ], 
                                width = 4),
                            dbc.Col([
                                dbc.Row([graph],  style={'padding': '0'}), 
                            ],
                                width = 8),
                            ]
                    ),

                    ### THIRD ROW ###
                    dbc.Row([
                            dbc.Col([
                                dbc.Row([events_ytd_card], class_name = 'm-2', 
                                        style={'padding': '0'}, ),
                            ], 
                                width = 4),
                            dbc.Col([
                                dbc.Row([graph],  style={'padding': '0'}), 
                            ],
                                width = 8),
                            ]
                    ),
                ],
                    id='targetRevenueRow', fluid=False
            )

    return target_revenue

target_revenue = get_target_revenue()

#################################################################
#                           LAYOUT                              #
#################################################################
def layout_home():
    sidebar = create_sidebar()
    home_layout = html.Div(
        [
            sidebar,
        #     children=[
        #         # html.H1("Home Page"),
        #         # html.P("Welcome to the Home Page!"),
        #         # select_menu,
            ### First section ##
            create_opex_card(),
        #         # opex_capex,
        #         html.Br(),
            html.Hr(),
            # row_3,
        #         html.Hr(),
        #         html.Br(),
        # Second section 
            target_revenue,
        #         html.Hr(),

        #         # select_menu,
        #     ]
        # )
        ],
        className='page-bg'
    )
    return home_layout

def layout_operation():
    return html.Div(
        children=[
            html.H1("👩🏻‍💼 Operation Page"),
            html.P("Welcome to the Novalearn Operations Page!", style={'textAlign':'center'}),
            html.Br(),
            events,
            target_revenue,
            ## LIST OF PROGRAMS ##
            # html.Div([
            #     html.H4("Upcoming Events"),
            #     html.Li("Events Upcoming"),
            #     html.H4("Ongoing Events"),
            #     html.Li([
            #          html.P("ASA ISNS"),
            #     ]),
            # ]),
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