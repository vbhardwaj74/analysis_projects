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
from Flask_Login_v2.dashapp1.layout import df2


def register_callbacks(dashapp):
    @app.callback([
        Output('final_table', 'children'),
        Output('line_chart', 'figure')],
        [Input('dropdown_d1', 'value'),
         Input('dropdown_d2', 'value')])
    def update_table(d1, d2):

        if (d1 != None and d2 != None):
            df_filtered = df2[df2["mobile_devices"].isin(d1) & df2["source"].isin(d2)]

        elif d1 != None:
            df_filtered = df2[df2["mobile_devices"].isin(d1)]

        elif d2 != None:
            df_filtered = df2[df2["source"].isin(d2)]

        else:
            df_filtered = df2

        dataTable = [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
            page_action='none',
            style_table={'height': '500px', 'overflowY': 'auto'}
        )]

        # list_chosen_devices=df_filtered['mobile_devices'].unique().tolist()
        # df_line = df2[df2['mobile_devices'].isin(list_chosen_devices)]
        df_line = df_filtered.groupby(['months', 'mobile_devices'])['visit_id'].sum().to_frame().reset_index()

        fig = px.line(df_line,
                      x="months",
                      y='visit_id',
                      color='mobile_devices',
                      height=600)
        fig.update_layout(yaxis={'title': 'visits'},
                          title={'text': 'visits MoM',
                                 'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'},
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