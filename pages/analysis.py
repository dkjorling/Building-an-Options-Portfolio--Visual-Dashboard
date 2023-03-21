import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import sys
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, register_page, callback
from datetime import datetime as dt
from datetime import date
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template

# .py file imports
import Performance_Stats as ps
import Visualization as vs

### Load Data ###
#path1 = '/Users/dylanjorling/UCLA/mas_thesis/data'
#tickers = pd.read_csv(path1+'/_data_vol_tickers')
#tickers = list(tickers.iloc[:, 1])
tickers = pd.read_csv('assets/tickers.csv')
tickers = list(tickers.iloc[:, 1])
                      

#path = '/Users/dylanjorling/UCLA/mas_thesis/results/dfs/'
#name = 'final_results.csv'
#data = pd.read_csv(path+name, index_col='date', parse_dates=True)
data = pd.read_csv('assets/final_results.csv', index_col='date', parse_dates=True)

IV = data.iloc[:, :315]
####################################################################################
op_style = {'color':'midnightblue', 'font-size':12}

model_options = [{'label':html.Span(['Attention Transformer'], style=op_style),
                  'value':'Attention Transformer'},
                 {'label':html.Span(['GRU'], style=op_style), 'value':'GRU'},
                 {'label':html.Span(['LSTM'], style=op_style), 'value':'LSTM'},
                 {'label':html.Span(['Baseline'], style=op_style), 'value':'Baseline'}]

model_to_column = {'Attention Transformer':'return_portfolio_attn',
                   'GRU':'return_portfolio_gru',
                   'LSTM':'return_portfolio_lstm',
                   'Baseline':'return_benchmark'}

st_style = {'color':'midnightblue'}

stat_options = [{'label':html.Span(['Return'], style=op_style), 'value':'Return'},
                {'label':html.Span(['Standard Deviation'], style=op_style), 'value':'Standard Deviation'},
                {'label':html.Span(['Sharpe Ratio'], style=op_style), 'value':'Sharpe Ratio'},
                {'label':html.Span(['Sortino Ratio'], style=op_style), 'value':'Sortino Ratio'},
                {'label':html.Span(['Max Drawdown'], style=op_style), 'value':'Max Drawdown'},
                {'label':html.Span(['Calmar Ratio'], style=op_style), 'value':'Calmar Ratio'}]

stat_to_function = {'Return':ps.total_return,
                    'Standard Deviation':ps.return_std,
                    'Sharpe Ratio':ps.sharpe_ratio,
                    'Sortino Ratio':ps.sortino_ratio,
                    'Max Drawdown':ps.max_drawdown,
                    'Calmar Ratio':ps.calmar_ratio}

window_options = [{'label':html.Span(['30d'], style=op_style), 'value':'30d'},
                  {'label':html.Span(['45d'], style=op_style),'value':'45d'},
                  {'label':html.Span(['60d'], style=op_style),'value':'60d'},
                  {'label':html.Span(['90d'], style=op_style),'value':'90d'},
                  {'label':html.Span(['180d'], style=op_style),'value':'180d'},
                  {'label':html.Span(['360d'], style=op_style),'value':'360d'}]


left_panel_style = {'padding':'5px 15px',
                   'border-right':'3px solid midnightblue'}

dropdown_style = {}

date_range_style = {'font-size':'12px',
                    'border' : '1px solid midnightblue',
                    'color':'midnightblue'}

style=date_range_style
####################################################################################
### Register Page Name for Multi-Page Layout ###
register_page(__name__)


load_figure_template('LUMEN')



### Begin Page Layout ###

layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.H2('Model Metrics',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
    ]),
    
    dbc.Row([
        dbc.Col(
            dbc.Stack([
                html.P("Select Metric:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="stat_dropdown-1",
                             options=stat_options,
                             value='Return',
                             style={'width': "95%"}),
                html.Br(),
                html.P("Date Range:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.DatePickerRange(min_date_allowed=date(2014, 1, 1),
                                    max_date_allowed=date(2022, 12, 31),
                                    initial_visible_month=date(2014, 1, 1),
                                    start_date=date(2014, 1, 1),
                                    end_date=date(2022, 12, 31),
                                    id='date-range-1',
                                    style=date_range_style),
                html.Br(),
                html.P("Select Model (Heatmap):", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="model_dropdown-1",
                             options=model_options,
                             value='Attention Transformer',
                             style={'width': "95%", 'height':'50%'}),],
                style={'padding':'0px 15px'}),
            style=left_panel_style
        ),
        dbc.Col(dcc.Graph(id="rolling_metric"), width = 5,
               style=left_panel_style),
        dbc.Col(dcc.Graph(id="return_heatmap"), width = 5),
    ]),
    
    dbc.Row([     
        dbc.Col(html.H2('Volatiliy Exposure and Long/Short IV Levels',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
    ]),
    
    dbc.Row([
        dbc.Col(
            dbc.Stack([
                html.P("Select Model:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="model_dropdown-2",
                             options=model_options[:3],
                             value='Attention Transformer',
                             style={'width': "95%"}),
                html.Br(),
                html.P("Select Window:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="window_dropdown-1",
                             options=window_options,
                             optionHeight=15,
                             value='30d',
                             style={'width': "95%",}),
                html.Br(),
                html.P("Date Range:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.DatePickerRange(min_date_allowed=date(2014, 1, 1),
                                    max_date_allowed=date(2022, 12, 31),
                                    initial_visible_month=date(2014, 1, 1),
                                    start_date=date(2014, 1, 1),
                                    end_date=date(2022, 12, 31),
                                    id='date-range-2'),],
                style={'padding':'0px 15px'}),
            style=left_panel_style
        ),
        dbc.Col(dcc.Graph(id="iv_exposure"), width = 10),
    ]),
    
    dbc.Row([
        dbc.Col(html.H2('Asset IV over time and Correlations',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
    ]),

    
    dbc.Row([
        dbc.Col(
            dbc.Stack([
                html.P("Select Assets:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="asset_dropdown-1",
                             options=tickers,
                             value=['AAPL', 'SPY'],
                             multi=True,
                             style={'width': "95%"}),
                html.Br(),
                html.P("Select Window:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="window_dropdown-2",
                                 options=window_options,
                                 value='30d',
                                 style={'width': "95%",}),],
                style={'padding':'0px 15px'}),
            style=left_panel_style
        ),
        dbc.Col(dcc.Graph(id="asset_corr"), width=5, style=left_panel_style),
        dbc.Col(dcc.Graph(id="asset_iv"), width=5),
    ]),
        
    dbc.Row([
        dbc.Col(style=left_panel_style),
        dbc.Col(dcc.RangeSlider(min=data.index[0].year,
                                max=data.index[-1].year,
                                value=[data.index[0].year, data.index[-1].year],
                                step=1,
                                vertical=False,
                                marks={str(year): str(year) for year in data.index.year.unique()},
                                id='year-slider-1'),
                width=10),
    ]),
    
    dbc.Row([
        dbc.Col(html.H2('Model Comparison',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
    ]),
    
    dbc.Row([
        dbc.Col(
            dbc.Stack([
                html.P("Date Range:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.DatePickerRange(min_date_allowed=date(2014, 1, 1),
                                    max_date_allowed=date(2022, 12, 31),
                                    initial_visible_month=date(2014, 1, 1),
                                    start_date=date(2014, 1, 1),
                                    end_date=date(2022, 12, 31),
                                    id='date-range-3'),
                html.Br(),
                html.P("Select Model:", style={'color':'midnightblue'}),
                html.Hr(style={'color':'midnightblue'}),
                dcc.Dropdown(id="model_dropdown-3",
                             options=model_options,
                             value='Attention Transformer',
                             style={'width': "95%"}),],
                style={'padding':'0px 15px'}),
            style=left_panel_style

        ),
        dbc.Col(dcc.Graph(id="port_values"), width=5, style=left_panel_style),
        dbc.Col(dcc.Graph(id="annual_returns"), width=5),
    ])

])
####################################################################################
@callback(
    Output('rolling_metric', 'figure'),
    Output('return_heatmap', 'figure'),
    Input('stat_dropdown-1', 'value'),
    Input('model_dropdown-1', 'value'),
    Input('date-range-1', 'start_date'),
    Input('date-range-1', 'end_date')
)

def update_figure_1(stat, model, date1, date2):
    stat_fcn = stat_to_function[stat]
    start = date1
    end = date2
    title = "Annualized Rolling " + stat
    
                  
    fig1 = vs.plot_rolling_metric([data['return_portfolio_lstm'],
                                  data['return_portfolio_attn'],
                                  data['return_portfolio_gru'],
                                  data['return_benchmark']],
                                 metric=stat_fcn,
                                 title=title,
                                 start=start,
                                 end=end)
    
    col = model_to_column[model]          
    fig2 = vs.return_matrix(data[col])
    
    
    
    return fig1, fig2

@callback(
    Output('iv_exposure', 'figure'),
    Input('model_dropdown-2', 'value'),
    Input('window_dropdown-1', 'value'),
    Input('date-range-2', 'start_date'),
    Input('date-range-2', 'end_date')
)

def update_figure_2(model, window, date1, date2):         
    fig = vs.plot_iv_exposure_level(data,
                                    model=model,
                                    window=window,
                                    start=date1,
                                    end=date2)

    return fig

@callback(
    Output('asset_iv', 'figure'),
    Output('asset_corr', 'figure'),
    Input('asset_dropdown-1', 'value'),
    Input('window_dropdown-2', 'value'),
    Input('year-slider-1', 'value')
)

def update_figure_3(assets, window, yrs):
    start='01-01-' + str(yrs[0])
    end='12-31-' + str(yrs[1])
    
    fig2 = vs.plot_asset_iv(IV,
                           tickers=assets,
                           window=window,
                           start=start,
                           end=end)
    
    fig1 = vs.correlation_heat(IV,
                              tickers=assets,
                              start=start,
                              end=end)
    
    
    return fig1, fig2
@callback(
    Output('port_values', 'figure'),
    Output('annual_returns', 'figure'),
    Input('date-range-3', 'start_date'),
    Input('date-range-3', 'end_date'),
    Input('model_dropdown-3', 'value'),
)

def update_figure_4(date1, date2, model):
    col = model_to_column[model]
    start = date1
    end = date2
    
    fig1 = vs.plot_cum_return([data['return_portfolio_lstm'],
                              data['return_portfolio_attn'],
                              data['return_portfolio_gru'],
                              data['return_benchmark']],
                             title='Model Portfolio Values',
                             start=start,
                             end=end)
    
    start_year = int(date1[:4])
    end_year = int(date2[:4])
    
    title = model + " Annual Returns"
    fig2 = vs.single_stat_bar_yearly(data,
                                    col=col,
                                    stat=ps.total_return,
                                    title=title,
                                    start_yr=start_year,
                                    end_yr=end_year)

    return fig1, fig2













