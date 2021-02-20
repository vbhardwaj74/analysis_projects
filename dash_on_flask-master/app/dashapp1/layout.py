import dash_core_components as dcc
import dash_html_components as html
from app.dashapp1.callbacks import *
import datetime

layout = html.Div([html.Div(className="section",
    children=[
        html.Button(
            id="enter-button",
            className="button is-large is-outlined",
            children=["Export JSON"],
        ),
        html.Div(
            id="download-area",
            className="block",
            children=[]
        )
    ]),
    dt.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.loc[:, df.columns != 'Description']],
        data=df.to_dict('rows'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 15,
        export_format="csv"
    ),
        html.Div([
            dcc.DatePickerRange(id='date_filter',
                                clearable=True,
                                with_portal=True,
                                initial_visible_month= datetime.datetime(2020, 8, 1),
                               )], id='container_date_filter', ),
        html.Div([
            html.Label('Strategy'),
            dcc.Dropdown(id='dropdown_d1', options=[{'label':x, 'value':x} for x in df.sort_values('Strategy')['Strategy'].unique()],
                         value=None, multi=True),
            html.Label('Product'),
                       dcc.Dropdown(id='dropdown_d2', options=[{'label': i, 'value': i} for i in df.sort_values('Strategy')['Product'].unique()],
                                    value=None, multi=True),
            html.Label('Type'),
            dcc.Dropdown(id='dropdown_d3', options=[{'label':x, 'value':x} for x in df.sort_values('Product')['Type'].unique()],
                     value=None, multi=True),
        ], style={'display': 'inline-block', 'width': '30%', 'margin-left': '7%'}),
            html.Div([
            html.Label('Price Slider'),
            html.Div(children=dcc.RangeSlider(id='price_slider',
                                              updatemode='drag',
                                              #value = [df["Price"].min(), df["Price"].max()],
                                              allowCross = False
                                             )),
            html.Div(children=html.Div(id='price_slider_vals')),
        ], id='container_price_slider',
                style={'display': 'inline-block', 'width': '30%', 'margin-left': '45%'} ),
            html.Div([
            html.Label('Qty Slider'),
            html.Div(children=dcc.RangeSlider(id='qty_slider',
                                              updatemode='drag',
                                              #value = [df["Qty"].min(), df["Qty"].max()],
                                              allowCross = False
                                             )),
            html.Div(children=html.Div(id='qty_slider_vals'), ),
        ], id='container_qty_slider',
                style={'display': 'inline-block', 'width': '30%', 'margin-left': '45%'} ),
            html.Div([
            html.Label('Impl. Vol Slider'),
            html.Div(children=dcc.RangeSlider(id='vol_slider',
                                              updatemode='drag',
                                              #value = [df["Impl. Vol"].min(), df["Impl. Vol"].max()],
                                              allowCross = False
                                             )),
            html.Div(children=html.Div(id='vol_slider_vals'), ),
        ], id='container_vol_slider',
                style={'display': 'inline-block', 'width': '30%', 'margin-left': '45%'} ),
    html.Div(id='datatable-interactivity-container'),
    html.Div(
)
            ])
















'''
layout = html.Div([
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

'''






'''
layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})
'''
