import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly

import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px

from scipy.interpolate import interp1d

# create graph for daily report

def local_daily_graph_gen(new_df, category):
    daily_data = []
    daily_data.append(go.Scatter(
                  x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')))
    
    layout = {
        'title' :'Daily ' + category +' in ' + new_df['County'].values[0],
        'title_font_size': 26,
        'height':450,
        'xaxis' : dict(
            title='Date',
            titlefont=dict(
            family='Courier New, monospace',
            size=24,
            color='#7f7f7f'
        )),
        'yaxis' : dict(
            title='Covid-19 cases',
            titlefont=dict(
            family='Courier New, monospace',
            size=20,
            color='#7f7f7f'
        )),
        }  
    
    figure = [{
        'data': daily_data,
        'layout': layout
    }]
    
    return figure


# create graph for daily report
def daily_graph_gen(new_df, category):
    daily_data = []
    daily_data.append(go.Scatter(
                  x=new_df['Date'], y=new_df['coronavirus'], name="Covid-19 daily report", line=dict(color='#f36')))
    
    layout = {
        'title' :'Daily ' + category +' in ' + new_df['Country'].values[0],
        'title_font_size': 26,
        'height':450,
        'xaxis' : dict(
            title='Date',
            titlefont=dict(
            family='Courier New, monospace',
            size=24,
            color='#7f7f7f'
        )),
        'yaxis' : dict(
            title='Covid-19 cases',
            titlefont=dict(
            family='Courier New, monospace',
            size=20,
            color='#7f7f7f'
        )),
        }  
    
    figure = [{
        'data': daily_data,
        'layout': layout
    }]
    
    return figure