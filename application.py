import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import sys
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, page_container, page_registry
from datetime import datetime as dt
from datetime import date
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template



# .py file imports
import Performance_Stats as ps
import Visualization as vs

################################################################################################################################
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Data Visuals", href="/analysis")),
                dbc.NavItem(dbc.NavLink("Documentation", href="/documentation")),
                dbc.NavItem(dbc.NavLink("About", href="/about"))
                
            ] ,
            color="light",
            light=True,
        ), 
    ])

    return layout


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUMEN])

application = app.server # added for amazon beanstalk

app.layout = html.Div(children=[
    dbc.Row([
        
        dbc.Col(html.H1('Implied Volatility Portfolio Optimization with Deep Learning',
                       style={"color": "white",
                             'padding':'0px 15px'}),
                style={'background-color': 'midnightblue'}),
        
        html.Br(),
    ]),
    
#    dbc.Row([
        
#        dbc.Col(html.H5('Visualization of UCLA MAS Program Thesis - Dylan Jorling',
#                       style={"color": "white",
#                             'padding':'0px 15px'}),
#                style={'background-color': 'midnightblue'}),
#        html.Br(),
#    ]),
    
    dbc.Row([Navbar()
            ]),
    
    
    

    page_container,

])

if __name__ == '__main__':
    application.run(debug=True, port=8080)  # port added for amazon beanstalk
                       