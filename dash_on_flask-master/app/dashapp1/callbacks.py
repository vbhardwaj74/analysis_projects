import os
import re
from datetime import datetime as dt
import dash_table as dt
import pandas as pd
import plotly.express as px
from dash.dependencies import Input
from dash.dependencies import Output, State
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

electronic_data = pd.read_csv(r"/Users/visualboardwalk/github/minsanity_projects/dash_on_flask-master/electronic_flow_data.csv")

df = electronic_data
df = df.replace(',','', regex=True)
df['Qty'] = df['Qty'].astype('float64')


# JSON EXPORT
def build_download_button(uri):
    """Generates a download button for the resource"""
    button = html.Form(
        action=uri,
        method="get",
        children=[
            html.Button(
                className="button",
                type="submit",
                children=["Export JSON"]
            )
        ]
    )
    # return button

def register_callbacks(dashapp):
    # BUILD PRICE SLIDER
    @dashapp.callback(Output('price_slider_vals', 'children'),
                  [Input('price_slider', 'value')])
    def build_price_slider(numbers):
        if numbers is None:
            raise PreventUpdate
        return '$' + ' to $'.join([str(numbers[0]), str(numbers[-1])])


    # BUILD QTY SLIDER
    @dashapp.callback(Output('qty_slider_vals', 'children'),
                  [Input('qty_slider', 'value')])
    def build_qty_slider(numbers):
        if numbers is None:
            raise PreventUpdate
        return '' + ' to '.join([str(numbers[0]), str(numbers[-1])])


    # BUILD IMPL. VOL SLIDER
    @dashapp.callback(Output('vol_slider_vals', 'children'),
                  [Input('vol_slider', 'value')])
    def build_qty_slider(numbers):
        if numbers is None:
            raise PreventUpdate
        return '' + ' to '.join([str(numbers[0]), str(numbers[-1])])


    # FILTER TABLE
    @dashapp.callback(Output('datatable-interactivity', 'data'),
                  [Input('price_slider', 'value'),
                   Input('qty_slider', 'value'),
                   Input('vol_slider', 'value'),
                   Input('date_filter', 'start_date'),
                   Input('date_filter', 'end_date'),
                   Input('dropdown_d1', 'value'),
                   Input('dropdown_d2', 'value'),
                   Input('dropdown_d3', 'value')])
    def filter_table(num1, num2, num3, start_date, end_date, d1, d2, d3):
        if (num1 != None and num2 != None and num3 != None):
            return df[df["Price"].isin(num1) & df["Qty"].isin(num2) & df["Impl. Vol"].isin(num3)].to_dict('rows')
        elif num1 != None:
            return df[df["Price"].between(num1[0], num1[-1])].to_dict('rows')
        elif num2 != None:
            return df[df["Qty"].between(num2[0], num2[-1])].to_dict('rows')
        elif num3 != None:
            return df[df["Impl. Vol"].between(num3[0], num3[-1])].to_dict('rows')
        if (d1 != None and d2 != None and d3 != None):
            return df[df["Strategy"].isin(num1) & df["Product"].isin(num2) & df["Type"].isin(num3)].to_dict('rows')
        elif d1 != None:
            return df[df["Strategy"].isin(d1)].to_dict('rows')
        elif d2 != None:
            return df[df["Product"].isin(d2)].to_dict('rows')
        elif d3 != None:
            return df[df["Type"].isin(d3)].to_dict('rows')
        else:
            raise PreventUpdate
        if (start_date != None and end_date != None):
            return df[df["Date"].between(start_date, end_date)].to_dict('rows')


    #UPDATE GRAPHS
    @dashapp.callback(
        Output('datatable-interactivity-container', "children"),
        Input('datatable-interactivity', "derived_virtual_data"),
        Input('datatable-interactivity', "derived_virtual_selected_rows"),
        )
    def update_graphs(rows, derived_virtual_selected_rows):
        # When the table is first rendered, `derived_virtual_data` and
        # `derived_virtual_selected_rows` will be `None`. This is due to an
        # idiosyncrasy in Dash (unsupplied properties are always None and Dash
        # calls the dependent callbacks when the component is first rendered).
        # So, if `rows` is `None`, then the component was just rendered
        # and its value will be the same as the component's dataframe.
        # Instead of setting `None` in here, you could also set
        # `derived_virtual_data=df.to_rows('dict')` when you initialize
        # the component.
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        dff = df if rows is None else pd.DataFrame(rows)

        colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
                  for i in range(len(dff))]

        return [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["Strategy"],
                            "y": dff[column],
                            "type": "bar",
                            "marker": {"color": colors},
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": column}
                        },
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            # check if column exists - user may have deleted it
            # If `column.deletable=False`, then you don't
            # need to do this check.
            for column in ["Price", "Qty", "Impl. Vol"] if column in dff
        ]


    @dashapp.callback(
        Output("download-area", "children"),
        [
            Input("enter-button", "n_clicks")
        ])

    def show_download_button(n_clicks):
        # turn text area content into file
        filename = f"{uuid.uuid1()}.txt"
        path = r"/Users/visualboardwalk/Documents/cogent_export"
        with open(path, "w") as file:
            file.write(df.to_json(orient="records", lines=True))
        uri = path
        return [build_download_button(uri)]


    @dashapp.server.route('/downloadable/<path:path>')
    def serve_static(path):
        root_dir = os.getcwd()
        return flask.send_from_directory(
            os.path.join(root_dir, 'downloadable'), path
        )

'''
survey_data = pd.read_csv('/Volumes/GoogleDrive/Shared drives/MediSprout/data/survey_data_nov2020')

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

desktop_df = survey_data.groupby(['months', 'parent_desktop', 'source', 'is_satisfied'])[
    'visit_id'].count().to_frame().reset_index()
mobile_df = survey_data.groupby(['months', 'mobile_devices', 'source', 'is_satisfied'])[
    'visit_id'].count().to_frame().reset_index()
mom_df = survey_data.groupby(['months', 'is_satisfied', 'source', 'rating'])[
    'visit_id'].count().to_frame().reset_index()

df1 = mom_df
df1['rating'] = df1['rating'].astype(int)
df2 = mobile_df
df3 = desktop_df


def register_callbacks(dashapp):
    @dashapp.callback([
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
'''

'''
def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        return {
            'data': [{
                'x': df.index,
                'y': df.Close
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
'''
