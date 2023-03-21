import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, register_page, get_asset_url
from dash_bootstrap_templates import load_figure_template

### Save Style ###
home_style = {'padding':'0px 15px'}


####################################################################################
### Register Page Name for Multi-Page Layout ###
register_page(__name__, path='/')


load_figure_template('LUMEN')

### Begin Page Layout ###
layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.H2('Project Overview',
                        style={"color": "white",
                              'padding':'0px 15px'}),
                style={'background-color':'midnightblue'}),
        html.Br(),
    ]),
    
    dbc.Row([
        html.Br(),
        
        html.P(['The idea behind this Master\'s Thesis project is a proof-of-concept for a potential options trading ',
                'portfolio strategy using state-of-the-art machine learning models. Due to the complexity of implementing an ',
                'options trading strategy, here we use the 60-day implied options volatility as a proxy for actual options ',
                'prices. When the portfolio takes a “position” in any asset, we assume the portfolio is either buying or ',
                'selling an at-the-money straddle. A straddle is a delta-neutral strategy where the PNL is determined by ',
                'the size of an underlying move rather than the direction.  Delta is measured as the change in option price ',
                'over a $1 move in the underlying asset. ']),
        html.Br(),
        
        html.P([' The approximately 60-day until expiration timeframe was chosen since these options are much less ', 
                'gamma-intensive than options closer to expiration. Gamma is measured as the change in options delta over a ',
                '$1 move in the underlying asset. Essentially all this means is that 60-day out options are much more ',
                'resilient in staying delta-neutral than closer to expiration options. The reason not to use anything further ',
                'out than a 60-day option is that 60-day options tend to maintain nearly the same liquidity as closer-to-',
                'expiration options. Once we get past three-month out options, liquidity becomes significantly reduced.  ']),
        html.Br(),
        
        html.P(['Using the implied volatility data, as well as various other options and underlying asset data, three ',
                'machine learning models were trained to maximize portfolio Sharpe Ratio: LSTM, GRU and Attention ',
                'Transformer. The Sharpe Ratio is a risk-adjusted return measure calculated as annualized return / ',
                'annualized standard deviation. Investors are often concerned not only of the return they are making, but ',
                'also the stability of these returns which is why return adjusted for risk is generally preferred to just ',
                'return. Results of the study are shown below:']),
        html.Br(),],
    
    style={'padding':'15px 15px'},
    
    ),
    
    dbc.Row([
        html.Img(src = get_asset_url('results_tab.png'),
                 style={'width':'50%'}),],
        style={'textAlign':'center',
              'padding':'0px 15px'},
    ),
    
    dbc.Row([
        html.Br(),
        
        html.P(['One key point is that costs are not being considered, which would immensely impact model performance. ',
                'However, this is a proof-of-concept project and hopefully the springboard for further research on the topic. ',
                'Use the analysis tab to dig deeper into the data and results. ']),
        html.Br(),],
        
        style=home_style
    ),

    
]) ## final container brackets do not move    
