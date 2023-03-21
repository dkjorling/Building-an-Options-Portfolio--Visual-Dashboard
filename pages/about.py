import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, register_page, get_asset_url
from dash_bootstrap_templates import load_figure_template

### Save Style ###
about_style = {'padding':'0px 15px'}


####################################################################################
### Register Page Name for Multi-Page Layout ###
register_page(__name__)


load_figure_template('LUMEN')

layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.H2('About the Author',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
        html.Br(),
    ]),
    
    dbc.Row([
        html.Br(),
        
        html.P('My name is Dylan Jorling and I am currently a 2nd year Masters of Applied Statistics student at UCLA.'),
        html.Br(),
    ],
    style={'padding':'15px 15px'}),
])