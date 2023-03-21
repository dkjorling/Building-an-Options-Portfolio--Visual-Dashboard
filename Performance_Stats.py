import numpy as np
import pandas as pd
import time
from datetime import datetime as dt


def total_return(return_col, annualized=True):
    r = (return_col + 1).cumprod()[-1] -1
    if annualized == True:
        days = (return_col.index[-1] - return_col.index[0]).days
        r = (r + 1) ** (1 / (days / 365)) - 1
    return r
        
def return_std(return_col, annualized = True):
    sd = return_col.std()
    if annualized:
        sd = return_col.std() * np.sqrt(251)
    return sd

def sharpe_ratio(return_col):
    """Returns annualized Sharpe Ratio"""
    ann_return = total_return(return_col, annualized=True)
    ann_std = return_std(return_col,annualized=True)
        
    return ann_return / ann_std

def sortino_ratio(return_col):
    """Returns annualized Sortino Ratio"""
    dwn_returns = return_col[return_col < 0]
    ann_return = total_return(return_col, annualized=True)
    ann_dwn_std = return_std(dwn_returns, annualized=True)
    
    return ann_return / ann_dwn_std

def max_drawdown(return_col):
    """Returns MDD over column"""
    # source of code: https://quant.stackexchange.com/questions/57703/implementation-of-maximum-drawdown-in-python-working-directly-with-returns
    
    cum_rets = (1 + return_col).cumprod() - 1
    nav = ((1 + cum_rets) * 100).fillna(100)
    hwm = nav.cummax()
    dd = nav / hwm - 1

    return min(dd)

def calmar_ratio(return_col):
    ann_return = total_return(return_col, annualized=True)
    mdd = max_drawdown(return_col)
    
    return ann_return / np.abs(mdd)

def compute_annual_stats(df, column, stat):
    start_yr = df.index[0].year
    end_yr = df.index[-1].year
    
    stats = []
    for yr in range(start_yr, end_yr+1):
        start = '01-01-' + str(yr)
        end = '01-01-' + str(yr+1)
        df_a = df.loc[start:end]
        stats.append(stat(df_a[column]))
    return stats



def turnover_cost(df_pred, tickers, bps=1):
    """Calculate costs from asset turnover"""
    df_pred = df_pred.sort_index(ascending=True)
    port_value = 1 # assume portfolio value = 1 after first time period
    costs = []
    cost_returns = []
    for i in range(df_pred.shape[0] - 1):
        cost_ticker = []
        for j, ticker in enumerate(tickers):
            asset_value_0 = port_value * df_pred[str(tickers[j]) + '_port_weight'][i]
            asset_value_1 = asset_value_0 * (1 + df_pred['return_next_' + str(tickers[j])][i])
            port_value_next = port_value * (1+df_pred['return_next_portfolio'][i])
            asset_value_next =  port_value_next * df_pred[str(tickers[j]) + '_port_weight'][i+1]        
            val_change = np.abs((asset_value_next - asset_value_1))
            cost = val_change * bps / 10000 * -1
            cost_ticker.append(cost)
        cost_sum = np.sum(cost_ticker)
        costs.append(cost_sum)
        cost_return = cost_sum / port_value
        cost_returns.append(cost_return)
        port_value *= (1 + df_pred['return_next_portfolio'][i] + cost_return)
    cost_returns.append(0)
    df_pred['cost_return_next'] = cost_returns
    df_pred['cost_return'] = df_pred['cost_return_next'].shift(1)
    df_pred['total_portfolio_return'] = df_pred['cost_return'] + df_pred['return_portfolio']
    return df_pred




            