#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import ipynb.fs
#from .full.app import app
#from .full.layouts import layout1, layout2, layout3
import dash
import dash_auth
import pandas as pd
import numpy as np
import sys, re
import plotly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jitcache import Cache
import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from pandas.tseries.offsets import *
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

survey_data = pd.read_csv(r'G:\Shared drives\MediSprout\data\survey_data_nov2020')

def parent_desktop(row):
    platform = row['platform']
    
    if row['is_mobile'] == 0:
        if bool(re.search('Mac', str(platform))) == True:
            return 'Mac OS'
        elif bool(re.search('Linux', str(platform))) == True:
            return 'Linux'
        elif bool(re.search('Windows', str(platform))) == True:
            return 'Windows'
        else:
            return 'NaN'
        
def mobile_devices(row):
    platform = row['platform']
    
    if row['is_mobile'] == 1:
        if bool(re.search('iPhone', str(platform))) == True:
            return 'iPhone'
        elif bool(re.search('iPad', str(platform))) == True:
            return 'iPad'
        elif bool(re.search('samsung', str(platform))) == True:
            return 'samsung'
        elif bool(re.search('vivo', str(platform))) == True:
            return 'vivo'
        elif bool(re.search('lenovo', str(platform))) == True:
            return 'lenovo'
        elif bool(re.search('LG', str(platform))) == True:
            return 'LG'
        elif bool(re.search('motorola', str(platform))) == True:
            return 'motorola'
        elif bool(re.search('Pixel', str(platform))) == True:
            return 'Google Pixel'
        elif bool(re.search('OnePlus', str(platform))) == True:
            return 'OnePlus'
        elif bool(re.search('Yulong', str(platform))) == True:
            return 'Yulong'
        elif bool(re.search('LGE', str(platform))) == True:
            return 'LGE'
        elif bool(re.search('TCL', str(platform))) == True:
            return 'TCL'
        elif bool(re.search('ZTE', str(platform))) == True:
            return 'ZTE'
        elif bool(re.search('Xiaomi', str(platform))) == True:
            return 'Xiaomi'
        elif bool(re.search('AlcatelOneTouch', str(platform))) == True:
            return 'AlcatelOneTouch'
        elif bool(re.search('HUAWEI', str(platform))) == True:
            return 'HUAWEI'
        elif bool(re.search('Amazon', str(platform))) == True:
            return 'Amazon'
        elif bool(re.search('ALCATEL', str(platform))) == True:
            return 'ALCATEL'
        elif bool(re.search('TINNO', str(platform))) == True:
            return 'TINNO'
        elif bool(re.search('BLU', str(platform))) == True:
            return 'BLU'
        elif bool(re.search('Alco', str(platform))) == True:
            return 'Alco'
        elif bool(re.search('Innovations', str(platform))) == True:
            return 'Innovations'
        elif bool(re.search('HMD', str(platform))) == True:
            return 'HMD/Nokia'
        elif bool(re.search('Sony', str(platform))) == True:
            return 'Sony'
        elif bool(re.search('HTC', str(platform))) == True:
            return 'HTC'
        elif bool(re.search('LENOVO', str(platform))) == True:
            return 'LENOVO'
        elif bool(re.search('asus', str(platform))) == True:
            return 'asus'
        elif bool(re.search('Alco', str(platform))) == True:
            return 'Alco'
        elif bool(re.search('LENOVO', str(platform))) == True:
            return 'LENOVO'
        else:
            return 'Other'

def classify_mobile_type(row):
    platform = row['platform']
    
    if row['is_mobile'] == 1:
        if bool(re.match('Apple iP\w*', str(platform))) == True:
            return 'iOS'
        else:
            return 'Android'
    else:
        return 'NA'
    
    return row

def parent_desktop(row):
    platform = row['platform']
    
    if row['is_mobile'] == 0:
        if bool(re.search('Mac', str(platform))) == True:
            return 'Mac OS'
        elif bool(re.search('Linux', str(platform))) == True:
            return 'Linux'
        elif bool(re.search('Windows', str(platform))) == True:
            return 'Windows'
        else:
            return 'NaN'

        
survey_data['mobile_type'] = survey_data.apply(lambda row: classify_mobile_type(row), axis=1)
survey_data['mobile_devices'] = survey_data.apply(lambda row: mobile_devices(row), axis=1)
survey_data['parent_desktop'] = survey_data.apply(lambda row: parent_desktop(row), axis=1)
survey_data['created_on'] = pd.to_datetime(survey_data['created_on'], format='%Y-%m-%d %H:%M:%S.%f')
survey_data['created_on_date'] = survey_data['created_on'].dt.date
survey_data['months'] = pd.to_datetime(survey_data['created_on'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m')


desktop_df = survey_data.groupby(['months', 'parent_desktop', 'source', 'is_satisfied'])['visit_id'].count().to_frame().reset_index()
mobile_df = survey_data.groupby(['months', 'mobile_devices', 'source', 'is_satisfied'])['visit_id'].count().to_frame().reset_index()
mom_df = survey_data.groupby(['months', 'is_satisfied', 'source', 'rating'])['visit_id'].count().to_frame().reset_index()

df1 = mom_df
df1['rating'] = df1['rating'].astype(int)
df2 = mobile_df
df3 = desktop_df


app = dash.Dash(__name__, external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css'])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    #dcc.Link('Go to Page 2', href='/page-2'),
])

app.layout = html.Div([
    html.Div([
        html.Label('mobile devices'),
        dcc.Dropdown(id='dropdown_d1', options=[{'label':x, 'value':x} for x in df2.sort_values('mobile_devices')['mobile_devices'].unique()], 
                     value=None, multi=True),
        html.Label('source'),
        dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df2.sort_values('mobile_devices')["source"].unique()],
                     value=None, multi=True)
    ]),
    html.Div(id="final_table", className="six columns"),
    html.Div([
        html.Div([
            dcc.Graph(id='line_chart'),
        ],className="six columns"),
        html.Div([
            dcc.RangeSlider(
                id="rangeslider",
                pushable=2,
                marks = {i: {'label': i} for i in df2['months']}
            )
        ], className="six columns")
    ])
])

#app.layout = html.Div([dropdown, final_table, line_chart], className="row")

@app.callback([
    Output('final_table','children'),
    Output('line_chart', 'figure')],
    [Input('dropdown_d1', 'value'),
     Input('dropdown_d2', 'value')])

def update_table(d1, d2):
    
    if(d1 != None and d2 != None):
        df_filtered = df2[df2["mobile_devices"].isin(d1) & df2["source"].isin(d2)]
        
    elif d1 != None:
        df_filtered = df2[df2["mobile_devices"].isin(d1)]
        
    elif d2 != None:
        df_filtered = df2[df2["source"].isin(d2)]
        
    else:
        df_filtered = df2
        
    dataTable = [dt.DataTable(
            id='table', 
            columns = [{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            page_action='none',
            style_table={'height': '500px', 'overflowY': 'auto'}
        )]
        
    #list_chosen_devices=df_filtered['mobile_devices'].unique().tolist()
    #df_line = df2[df2['mobile_devices'].isin(list_chosen_devices)]
    df_line = df_filtered.groupby(['months', 'mobile_devices'])['visit_id'].sum().to_frame().reset_index()
    
    fig = px.line(df_line, 
                      x="months", 
                      y='visit_id', 
                      color='mobile_devices', 
                      height=600)
    fig.update_layout(yaxis={'title':'visits'},
                      title={'text':'visits MoM',
                      'font':{'size':28},'x':0.5,'xanchor':'center'},
                     autosize=False, height=500,
                      xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=3,
                    label="3m",
                    step="month",
                    stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
                     )
    
    return dataTable, fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


# SINGLE PAGE TEMPLATE

# In[ ]:




