import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

import os, math
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px

from pathlib import Path
dir = Path(__file__).parent
print (os.getcwd())
# os.chdir(dir)
#
Notion_db_content = 'https://www.notion.so/novalearn/b194bb2c04b1444084d1c3610d8bc672?v=0a63faf0c5074a9d9240e5a7f9c7a869&pvs=4'
courses_raw = pd.read_csv('data/All Courses b194bb2c04b1444084d1c3610d8bc672.csv')

n_signups = 44
b2b_sales = '$ 3000'
b2c_sales = '$ 800'
weekly_rev = '$ 540'

avg_cost_per_course = '$ 20'
number_of_active_users = '60'
number_of_events_ytd = 10
number_of_courses_published = 67
number_rtu_courses = 7

opex_value = '$20 000'
capex_value = '$5 000'
image_width = '50px'
image_height = '50px'

def preprocess_courses(courses_raw:pd.DataFrame) -> pd.DataFrame:

    courses_raw.columns = [x.lower().replace(' ', '_') for x in courses_raw.columns]
    # Courses
    
    courses_by_status = courses_raw.groupby('subject')['status'].value_counts().to_frame()#.reset_index()
    courses_by_status.columns = ['n_course']
    courses_by_status = courses_by_status.reset_index(drop=False)

    return courses_by_status

def get_courses_barchart(courses_by_status: pd.DataFrame, time_filter=None):

    courses_by_status = preprocess_courses(courses_raw)
    
    color_mapping = {
    'Published': '#0b912a',
    'Planning': '#5aa3de',
    'Ready For Editing': '#939ca3',
    'Editing': '#595169',
    'Scripts Complete': '#636c77',
    'Writing Scripts': '#2f4b70',
    'Ready For Scripts': '#7fe897',
    'Ready To Upload': '#D9e865',
    }
    
    fig = px.bar(courses_by_status, x='subject', color='status', y='n_course', barmode='group', color_discrete_map=color_mapping)
    fig.update_layout( plot_bgcolor='rgba(0, 0, 0, 0)',
                      xaxis=dict(
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True
                        ),
                    yaxis=dict(
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True
                        ),
                    xaxis_title = 'Subjects',
                    yaxis_title = '# of courses'
      )

    return fig

#################################################################
#                   COMPONENETS                                 #
#################################################################
# Radial shape components
def create_radial_component(planned_profit, target_profit):
    # Calculate the percentage of planned profit achieved
    percentage = (planned_profit / target_profit) * 100
    
    # Set the color of the radial shape based on the achievement percentage
    color = 'green' if percentage >= 80 else 'red'
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
                # dbc.Col(
                #         html.Img(src="assets/Opex.png", className="rounded-img", style={"height": "100px", "width": "100px"}),
                #         width=3, 
                #         ),
                dbc.Col(
                    html.P("80 000", className="card-text-header1"),
                    width=12
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
                # dbc.Col(
                #         html.Img(src="assets/Capex.png", className="rounded-img", style={"height": "100px", "width": "100px"}),
                #         width=2
                #         ),
                dbc.Col(
                    html.P("12 000", className="card-text-header1"),
                    width= 12
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
        create_radial_component(9_000, 10_000)
    ])

    ## 
    if Category == 'Sales':
        # New Signups
        new_signups = dbc.Card([
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H5("New Signups (month)", className="card-text-header2", 
                        # style={"text-align": "center",  # Set text alignment to center
                        #         "color": "white"} ,
                        ),
                html.P(
                    f"{n_signups} ",
                    className="card-text-body2",
                ),
            ],
            id = "new_signups")
        ], className="sales-card")

        # B2B Sales
        new_sales_revenue = dbc.Card([
            # dbc.CardHeader(f"{Category.upper()}"),
            dbc.CardBody([
                html.H5("New Sales Revenue", className="card-text-header2",
                    ),
                html.P(
                    f"{weekly_rev}",
                    className="card-text-body2",
                ),
            ],
            id = "new_sales_revenue")
        ], className="sales-card")

        # B2C Sales
        b2c_revenue = dbc.Card([
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
            id = "b2c_sales")
        ], className="sales-card")

        # dynamic Sales
        b2b_revenue = dbc.Card([
                dbc.CardBody([
                html.H5("B2B Sales", className="card-text-header2"),
                html.P(
                    f"{b2b_sales}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "weekly_rev")
        ], className="sales-card")


        row_3 = dbc.Container([
                    ### HEADER ROW ###
                    # dbc.Row(
                    #     dbc.Col(
                    #             html.H2("Sales by Business 💰", className='page-header'),
                    #             # width={"size": 12, "align":'stretch', "color":'#fffbfb'},
                    #     ),
                    #     justify='center',
                    # ),

                    dbc.Row([
                        dbc.Col([
                            dbc.Row([b2b_revenue],  className="m-2",), 
                            dbc.Row([b2c_revenue], className = "m-2"),
                            # dbc.Row([new_sales], className = "m-2"),
                        ], 
                            width = 4),
                        # html.Div(style={'border-left': '5px solid #efededa1', 'height': '100%'}, className='verticalline'),
                        # dbc.Col([], width=1) #insert space,
                        dbc.Col([
                            dbc.Row([new_signups], className = "m-2"), 
                            dbc.Row([new_sales_revenue], className = "m-2"), 
                            # dbc.Row([graph],  style={'padding': '0'}), 
                                ],
                                width = 4),

                        dbc.Col([
                            dbc.Row([planned_vs_kpi], class_name = 'm-2',)
                        ],
                        width= 4),
                        # html.Hr(), html.Div(className="verticalline")
                        
                        # dbc.Col([], width=3),
                    ],
                    align='end',
                ),
                ],
                id='CardRow', 
                className='custom-container',
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

# Progress Bar
time_slicer = dbc.Container([
        dbc.Row(
            dbc.Col(
                html.Div(
                children=[
                    html.H5("Select a timeline slicer", className="timeline-text"),
                    dcc.Dropdown(id='time-filter',
                                options= [
                                {'label': '1 Month', 'value': '1 month'}, 
                                {'label': '3 Months', 'value': '3 month'}, 
                                {'label': '6 Months', 'value': '6 month'}, 
                                ],
                                value = '1 month'), # default selected option
                        ],
                ),
                width={"size": 2, 'offset': 8}
            )
        )
 ])

def update_progress_bar(n_clicks):
    
    print (n_clicks)
    if n_clicks == '1 month':
        tempVal = 3  
        print (tempVal)
    else:
        tempVal = 20
    
    progress_bar = dbc.Progress(
                            value=tempVal,
                            max=100,
                            )
    # progress_bar_component = dbc.Container([
    #     html.Div(
    #     children=[
    #         progress_bar
    #     ],)
    # ], id='progressBar')
    progress_bar_component = dbc.Container([
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(children=[progress_bar]),
                                        width = {"size": 3, "offset": 3},
                                    ),
                                ),
                                ], id='progressBar')

    return progress_bar_component

pb = update_progress_bar(n_clicks=None)

placeholder = dbc.Container([
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
########################################################
#              COMPONENTS CREATIVE BOTTOM              #
########################################################

def get_courses_chart(courses_raw, time_filter=None):
    
    courses_by_status = preprocess_courses(courses_raw)
    print (f'--------------- Courses------  {time_filter}')
    # Create a graph component
    courses_graph = dcc.Graph(
        figure = get_courses_barchart(courses_by_status),
        style = {'height': "800px"}
    )
    # Position graph within the container
    courses_chart = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(children=[courses_graph] 
                )
            ]
            ),

        ],
        id='CoursesTracker',
        className='custom-container',
    )

    return courses_chart

month_slider = html.Div([
    dcc.Slider(
        id='monthRange',
        min=0,
        max=12,
        step=3,
        value=3
    ),   
], id='monthRange')
courses_chart = get_courses_chart(courses_raw)

def get_target_revenue():
    # 3 rows, 2 columns. Each row: Card LHS || Area Chart RHS

    ## CARDS : 3 samples (avg revenue per course, number of active users, # of events YTD)
    avg_revenue_card = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("Avg Cost / course", className="card-text-header2"), 
                    html.P(
                        f"{avg_cost_per_course} ",
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

    course_published = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("# Courses Published", className="card-text-header2"), 
                            # style={"text-align": "center",  # Set text alignment to center
                            #         "color": "white"} ,),
                    html.P(
                        f"{number_of_courses_published} ",
                        # style={"text-align": "center",
                        #         "color": "white"}, # Set text alignment to center
                        className="card-text-body2",
                    ),
                ],
                id = "course_published")
            ], className="sales-card")
    
    rtu_courses = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                dbc.CardBody([
                    html.H5("# Courses Ready to upload", className="card-text-header2"), 
                            # style={"text-align": "center",  # Set text alignment to center
                            #         "color": "white"} ,),
                    html.P(
                        f"{number_rtu_courses} ",
                        # style={"text-align": "center",
                        #         "color": "white"}, # Set text alignment to center
                        className="card-text-body2",
                    ),
                ],
                id = "rtu_courses")
            ], className="sales-card")
    
    upcoming_asa = dbc.Card([
                dbc.CardBody([
                html.H5("Upcoming # of ASA", className="card-text-header2"),
                html.P(
                    f"{3}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "upcoming_asa")
        ], className="sales-card")

    
    ##########################################################
    #       Chart the 3 rows, LHS Card, RHS Graph            #
    ##########################################################
    target_revenue = dbc.Container([
                        ### HEADER ROW ###
                        # dbc.Row(
                        #     dbc.Col(
                        #             html.H2("Other KPI 🏆", className='page-header'),
                        #             # width={"size": 12, "align":'stretch', "color":'#fffbfb'},
                        #     ),
                        #     justify='center',
                        # ),

                        ### FIRST ROW ###
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([avg_revenue_card], 
                                        class_name = "m-2", 
                                        style={'padding': '0'}, ),
                                # dbc.Row([graph],  style={'padding': '0'}), 
                            ], 
                                width = 4),

                            dbc.Col([
                                dbc.Row([n_active_card], className = "m-2", 
                                        style={'padding': '0'}, ),
                            ],
                                    width = 8),
                        ]
                    ),

                    ### SECOND ROW ###
                    dbc.Row([
                            dbc.Col([
                                dbc.Row([events_ytd_card], class_name = 'm-2', 
                                        style={'padding': '0'}, ),
                            ], 
                                width = 4),
                            dbc.Col([
                                dbc.Row([upcoming_asa], className = "m-2", 
                                        style={'padding': '0'}, ),
                            ],

                                width = 8),
                            ]
                    ),

                    ### THIRD ROW ###
                    dbc.Row([
                            dbc.Col([
                                dbc.Row([course_published], class_name = 'm-2', 
                                        style={'padding': '0'}, ),
                            ], 
                                width = 4),
                            dbc.Col([
                                # dbc.Row([graph],  style={'padding': '0'}), 
                                dbc.Row([rtu_courses], className = "m-2", 
                                        style={'padding': '0'}, ),
                            ],
                                width = 8),
                            ]
                    ),
                ],
                    id='targetRevenueRow', fluid=False
            )

    return target_revenue

target_revenue = get_target_revenue()

## CARDS : 3 samples (avg revenue per course, number of active users, # of events YTD)
def get_ceo_customer_cards():
    demo_conversion = '30 %'
    enquiries_conversion = '5 %'
    nps_score = '7/10'
    ttr = '< 24 hrs'

    # dynamic Sales
    demo_conversion = dbc.Card([
                dbc.CardBody([
                html.H5("Demo Conversion", className="card-text-header2"),
                html.P(
                    f"{demo_conversion}",
                    className="card-text-body2",
                ),
            ],
            id = "demo_conversion")
        ], className="flex-box card-style no-header-card sales-card")

    enquiries_conversion = dbc.Card([
                dbc.CardBody([
                html.H5("Enquiries Conversion", className="card-text-header2"),
                html.P(
                    f"{enquiries_conversion}",
                    className="card-text-body2",
                ),
            ],
            id = "enquiry_conversion")
        ], className="flex-box card-style no-header-card sales-card")

    nps_scoring = dbc.Card([
                dbc.CardBody([
                html.H5("Net Promoter Score", className="card-text-header2"),
                html.P(
                    f"{nps_score}",
                    className="card-text-body2",
                ),
            ],
            id = "nps_scoring")
        ], className="flex-box card-style no-header-card sales-card")
    
    time_to_response = dbc.Card([
                dbc.CardBody([
                html.H5("Time to Respond to Request", className="card-text-header2"),
                html.P(
                    f"{ttr}",
                    className="card-text-body2",
                ),
            ],
            id = "time_to_response")
        ], className="flex-box card-style no-header-card sales-card")
    
    return demo_conversion, enquiries_conversion, nps_scoring, time_to_response

def get_ceo_b2b_cards():
    # dynamic Sales
    B2B_REVENUE = dbc.Card([
            dbc.CardBody([
            html.H5("B2B Sales", className="card-text-header2"),
            html.P(
                f"{b2b_sales}",
                # style={"text-align": "center",  # Set text alignment to center
                #         "color": "white"} , # Set text alignment to center
                className="card-text-body2",
            ),
        ],
        id = "weekly_rev")
    ], className="flex-box card-style no-header-card sales-card")

     # dynamic Sales
    B2C_REVENUE = dbc.Card([
            dbc.CardBody([
            html.H5("B2C Sales", className="card-text-header2"),
            html.P(
                f"{b2c_sales}",
                # style={"text-align": "center",  # Set text alignment to center
                #         "color": "white"} , # Set text alignment to center
                className="card-text-body2",
            ),
        ],
        id = "weekly_rev")
    ], className="flex-box card-style no-header-card sales-card")

    return B2B_REVENUE, B2C_REVENUE

def get_ceo_talent_cards():
    
    # Number of Formal Trainings + Accreditions
    professional_upskil = 10
    n_turnover = 0
    n_sales_lead = 2

    human_development = dbc.Card([
                dbc.CardBody([
                html.H5("People Building", className="card-text-header2"),
                html.P(
                    f"{professional_upskil}",
                    className="card-text-body2",
                ),
            ],
            id = "professional_upskill")
        ], className="flex-box card-style no-header-card sales-card")
    
    employee_turnover = dbc.Card([
                dbc.CardBody([
                html.H5("Employee Turnover", className="card-text-header2"),
                html.P(
                    f"{n_turnover}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "employee_turnover")
        ], className="flex-box card-style no-header-card sales-card")

    growth_expansion = dbc.Card([
                dbc.CardBody([
                html.H5("Growth Expansion", className="card-text-header2"),
                html.P(
                    f"{n_sales_lead}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "sales_education_growth")
        ], className="flex-box card-style no-header-card sales-card")
    
    bonus_card = dbc.Card([
                dbc.CardBody([
                html.H5("📢 Bonus! Important! 🎁", className="card-text-header2"),
                html.P(
                    "ASA week!",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "sales_education_growth")
        ], className="flex-box card-style no-header-card sales-card")
    
    return human_development, employee_turnover, growth_expansion, bonus_card

def get_kpi_titles():
    """ 
    Plots as per new KPI Dashboard
    """
    FINANCIALS = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/dollar.png", top=True, style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("FINANCIALS STREAM", className="card-text-header2"), 
                        ],
                    id = "financials_card"),
                ],
                className="flex-box card-style no-header-card financials-card")

    CUSTOMER = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/rating.png", top=True, style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("CUSTOMER CENTRICITY", className="card-text-header2"), 
                        ],
                    id = "customer_centric"),
                ],
                className="flex-box card-style no-header-card customer-card")

    TALENT_MGT = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/talent-management.png", top=True,  style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("TALENT MANAGEMENT", className="card-text-header2"), 
                        ],
                    id = "talent_management"),
                ],
                className="flex-box card-style no-header-card talent-card")

    ######################################################################
    #                   CEO KPI                                          #
    ######################################################################
    # B2B, B2C
    B2B_REVENUE, B2C_REVENUE = get_ceo_b2b_cards()

    # New Signups
    new_signups = dbc.Card([
        # dbc.CardHeader(f"{Category.upper()}"),
        dbc.CardBody([
            html.H5("New Signup", className="card-text-header2", 
                    ),
            html.P(
                f"{n_signups} ",
                className="card-text-body2",
            ),
        ],
        id = "new_signups")
    ], className="flex-box card-style no-header-card sales-card")

    # New Sales
    new_sales_revenue = dbc.Card([
        # dbc.CardHeader(f"{Category.upper()}"),
        dbc.CardBody([
            html.H5("New Sales", className="card-text-header2",
                ),
            html.P(
                f"{weekly_rev}",
                className="card-text-body2",
            ),
        ],
        id = "new_sales_revenue")
    ], className="flex-box card-style no-header-card sales-card")

    ## Customer cards ##
    demo_conversion, enquiry_conversion, nps_score, ttr = get_ceo_customer_cards()

    ## Talent Management & Sales Growth ##
    human_development, employee_turnover, growth_expansion, bonus_card = get_ceo_talent_cards()
    
    ##########################################################
    #       Chart the 3 rows, LHS Card, RHS Graph            #
    ##########################################################
    ### FIRST ROW ###
    title_cards = dbc.Container([
        dbc.Row([
            # First Col, 3 rows
                dbc.Col([
                    html.Div([FINANCIALS], style={'margin-bottom': '15px'}),
                    html.Div([CUSTOMER], style={'margin-bottom': '15px'}),
                    html.Div([TALENT_MGT], style={'margin-bottom': '10px'}),
                    # dbc.Row([FINANCIALS], 
                    #         class_name = "flex-box", 
                    #         style={'padding': '2'}, ),
                    # dbc.Row([CUSTOMER], className = "flex-box", 
                    #         style={'padding': '2'}, ),
                    # dbc.Row([TALENT_MGT], className = "flex-box", 
                    #         style={'padding': '2'}, ),
                    ],xs = 4),
                #############################################################
                #           KPI VALUE CARDS LEVERS HERE                     #
                #############################################################
                # 4 columns in first Financials Categories.

                dbc.Col([
                    # B2b revenue
                    html.Div([B2B_REVENUE], style={'margin-bottom': '15px'}),
                    # dbc.Row([B2B_REVENUE],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                    # nps_score
                    html.Div([nps_score], style={'margin-bottom': '15px'}),
                    # dbc.Row([nps_score],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),  
                    # human_development
                    html.Div([human_development], style={'margin-bottom': '15px'}),
                    # dbc.Row([human_development],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),   
                ],
                xs = 2),
                dbc.Col([
                    # B2C revenue
                    html.Div([B2C_REVENUE], style={'margin-bottom': '10px'}),
                    # dbc.Row([B2C_REVENUE],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}), 
                    # demo conversion
                    html.Div([demo_conversion], style={'margin-bottom': '10px'}),
                    # dbc.Row([demo_conversion],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                    # employee_turnover
                    html.Div([employee_turnover], style={'margin-bottom': '15px'}),
                    # dbc.Row([employee_turnover],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                ],
                xs = 2),
                dbc.Col([
                    # new sales revenue
                    html.Div([new_sales_revenue], style={'margin-bottom': '10px'}),
                    # dbc.Row([new_sales_revenue],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}, align="center"),
                    # enquiry conversion
                    html.Div([enquiry_conversion], style={'margin-bottom': '10px'}),
                    # dbc.Row([enquiry_conversion],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                    # growth_expansion
                    html.Div([growth_expansion], style={'margin-bottom': '10px'}),
                    # dbc.Row([growth_expansion],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                ],
                xs = 2),
                dbc.Col([
                    # new signups
                    html.Div([new_signups], style={'margin-bottom': '10px'}),
                    # dbc.Row([new_signups],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),
                    # Time to response
                    html.Div([ttr], style={'margin-bottom': '10px'}),
                    # dbc.Row([ttr],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),   
                    # Bonus Card
                    html.Div([bonus_card], style={'margin-bottom': '10px'}),
                    # dbc.Row([bonus_card],
                    #         class_name="m-2",
                    #         style= {'padding': '2'}),  
                ],
                xs = 2),

                ]),
    ],
    fluid=True)
    
    return title_cards

title_cards = get_kpi_titles()

############################################
#           PRODUCT HEADER                 #
############################################
def get_tech_kpi_cards():
    # Number of Formal Trainings + Accreditions
    platform_costs = 3897
    user_acquisition_cost = 30
    n_sales_lead = 2
    n_projects_pipeline = 4

    platform_costs = dbc.Card([
                dbc.CardBody([
                html.H5("Platform cost YTD (U$D)", className="card-text-header2"),
                html.P(
                    f"{platform_costs}",
                    className="card-text-body2",
                ),
            ],
            id = "platform_cost")
        ], className="flex-box card-style no-header-card sales-card")
    
    conversion_cost = dbc.Card([
                dbc.CardBody([
                html.H5("User Acq. Cost U$D", className="card-text-header2"),
                html.P(
                    f"{user_acquisition_cost}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "user_acquisition")
        ], className="flex-box card-style no-header-card sales-card")

    n_project = dbc.Card([
                dbc.CardBody([
                html.H5("Product Dev Pipeline", className="card-text-header2"),
                html.P(
                    f"{n_projects_pipeline}",
                    # style={"text-align": "center",  # Set text alignment to center
                    #         "color": "white"} , # Set text alignment to center
                    className="card-text-body2",
                ),
            ],
            id = "n_project_pipeline")
        ], className="flex-box card-style no-header-card sales-card")
    
    # product_sales = dbc.Card([
    #             dbc.CardBody([
    #             html.H5("📢 Bonus! Important! 🎁", className="card-text-header2"),
    #             html.P(
    #                 "ASA week!",
    #                 # style={"text-align": "center",  # Set text alignment to center
    #                 #         "color": "white"} , # Set text alignment to center
    #                 className="card-text-body2",
    #             ),
    #         ],
    #         id = "sales_education_growth")
    #     ], className="flex-box card-style no-header-card sales-card")
    
    return platform_costs, conversion_cost, n_project#, bonus_card

def get_tech_headers():
    FINANCIALS = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/dollar.png", top=True, style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("FINANCIALS STREAM", className="card-text-header2"), 
                        ],
                    id = "financials_card"),
                ],
                className="flex-box card-style no-header-card financials-card")

    PLATFORM = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/rating.png", top=True, style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("CUSTOMER CENTRICITY", className="card-text-header2"), 
                        ],
                    id = "customer_centric"),
                ],
                className="flex-box card-style no-header-card customer-card")

    USER = dbc.Card([
                # dbc.CardHeader(f"{Category.upper()}"),
                    dbc.CardImg(src="assets/sidebar/gauge-chart.png", top=True,  style={'width': image_width, 'height': image_height, 'margin': 'auto'}),
                    dbc.CardBody([
                        html.H5("PLATFORM MANAGEMENT", className="card-text-header2"), 
                        ],
                    id = "talent_management"),
                ],
                className="flex-box card-style no-header-card talent-card")
    
    return PLATFORM, USER, FINANCIALS

def get_tech_kpi():
    # Get headers
    PLATFORM, USER, FINANCIALS = get_tech_headers()

    # Get score cards
    platform_costs, conversion_cost, n_project = get_tech_kpi_cards()

    ### FIRST ROW ###
    tech_cards = dbc.Container([
        dbc.Row([
            # First Col, 3 rows
                dbc.Col([
                    html.Div([FINANCIALS], style={'margin-bottom': '15px'}),
                    html.Div([PLATFORM], style={'margin-bottom': '10px'}),
                    html.Div([USER], style={'margin-bottom': '15px'}),
                    # dbc.Row([FINANCIALS], 
                    #         class_name = "flex-box", 
                    #         style={'padding': '2'}, ),
                    # dbc.Row([CUSTOMER], className = "flex-box", 
                    #         style={'padding': '2'}, ),
                    # dbc.Row([TALENT_MGT], className = "flex-box", 
                    #         style={'padding': '2'}, ),
                    ],xs = 4),

                     #############################################################
                #           KPI VALUE CARDS LEVERS HERE                     #
                #############################################################
                # 4 columns in first Financials Categories.

                dbc.Col([
                    # Platform cost
                    html.Div([platform_costs], style={'margin-bottom': '15px'}),
                    # Conversion Score
                    html.Div([conversion_cost], style={'margin-bottom': '15px'}),
                    # Project pipeline
                    html.Div([n_project], style={'margin-bottom': '15px'}),
                ],
                xs = 6),

                ]),
    ],
    fluid=True)

    return tech_cards

tech_cards = get_tech_kpi()

#################################################################
#                           LAYOUT                              #
#################################################################
def layout_home():
    sidebar = create_sidebar()
    home_layout = html.Div(
        [
            ### Test new section:
            get_kpi_titles()
        ],
        className='page-bg'
    )
    return home_layout

def layout_marketing():
    return html.Div(
        children=[
            html.H1(" Marketing Page", className='page-header'),
            html.Br(),
            placeholder,
            target_revenue,
            time_slicer,
            pb,
        ],
        className='page-bg'
        
    )


def layout_creative():
    return html.Div(
        children=[
            html.H1("🎨 Creative and Content Page", className='page-header'),
            html.Br(),
            target_revenue,
            html.H3("Subjects published till date", className='header2'),
            html.Br(),
            time_slicer,
            courses_chart,
        ],
        className='page-bg'
    )

def layout_product():
    return html.Div(
        children=[
            ### Test new section:
            tech_cards,

        ],
        id="PRODUCT_PAGE",
        className='page-bg'

    )