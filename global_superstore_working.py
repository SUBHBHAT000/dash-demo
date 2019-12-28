# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 05:29:23 2019

@author: Home-PC
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input,Output
import pandas as pd
import json

def generate_table(dataframe, max_rows=10, show_index = True):
    if show_index:
        return html.Table(
            # Header
            [html.Tr([html.Th(dataframe.index.name)] + [html.Th(col) for col in dataframe.columns])] +

            # Body
            [html.Tr([html.Td(dataframe.index[i])] + [
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )
    else:
        return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )

def get_marker(useMarker):
    bar_color = ['#0524ad', '#052099', '#041b80', '#031563', '#02104f', '#020a30']
    if useMarker:
        return dict(color = bar_color)
    else:
        return None
    
def get_text_font():
    return dict(
                family='Courier New, monospace',
                size=20,
                color='#e1e4f2'
                )
    
def get_graph_layout(graphTitle,
                     graphWidth,
                     graphHeight,
                     graphHoverMode,
                     marginLeft,
                     marginRight,
                     marginTop,
                     marginBottom,
                     graphFontFamily,
                     graphFontSize,
                     graphFontColor,
                     xAxisTitle,
                     yAxisTitle,
                     axisFontFamily,
                     axisFontSize,
                     axisFontColor):
    return {'title'    :graphTitle,
            'margin'   : dict(l=marginLeft, r=marginRight, t=marginBottom, b=marginBottom),
            'height'   : graphHeight,
            'width'    : graphWidth,
            'hovermode': graphHoverMode,
            'font' : dict(
                          family= graphFontFamily,
                          size  = graphFontSize,
                          color = graphFontColor
                          ),
            'xaxis': dict(
                          title = xAxisTitle,
                          titlefont=dict(
                                          family = axisFontFamily,
                                          size  = axisFontSize,
                                          color = axisFontColor
                                          )
                      ),
             'yaxis': dict(
                          title = yAxisTitle,
                          titlefont=dict(
                                          family = axisFontFamily,
                                          size  = axisFontSize,
                                          color = axisFontColor
                                          )
                      )
              }
        
data_set = 'C:/PythonTutorial/Python_Dash/project_global_superstore/Global Superstore.xls'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Global Super Store'

app.layout = html.Div([
                html.Div([
                        html.H1(children = 'Global Super Store')
                        ],className="banner"),
                html.Div([
                        html.Div([
                                dcc.Dropdown(id='top-n-cust-option',options = [{'label': f'Top {i} customers by sale','value':i} for i in range(5,21)],value = 5)
                                ],className = 'two columns'),
                        html.Div([
                                html.Button(id='top-n-cust-sumbit',n_clicks=0,children='submit')
                                ],className = 'one columns'),
                        html.Div([
                                #html.H1('1.3')
                                ],className = 'nine columns')
                        ],className="twelve columns"),
                html.Div([
                        html.Div([
                                html.H2('2.1 - Top N customers by Sale'),
                                dcc.Graph(id = 'graph-bar-top-n-cust')
                                ],className = 'six columns'),
                        html.Div([
                                html.H2('2.2 - Sale by category for the customer'),
                                dcc.Graph(id = 'graph-bar-cust-sale-by-category')
                                ],className = 'six columns'),
                        ],className="twelve columns"),
                html.Div([
                        html.H3('Section 3'),
                        dcc.Graph()
                        ],className="row"),
                html.Div([
                        html.Div([
                                html.H4('Section 4.1'),
                                dcc.Graph()
                                ],className="three columns"),
                        html.Div([
                                html.H4('Section 4.2'),
                                dcc.Graph()
                                ],className="three columns"),
                        html.Div([
                                html.H4('Section 4.3'),
                                dcc.Graph()
                                ],className="three columns"),
                        html.Div([
                                html.H4('Section 4.4'),
                                dcc.Graph()
                                ],className="three columns"),
                        ],className="row"),
                html.Div(id = 'selected-data'),
                html.Div(id = 'hidden-div', style = {'display': 'none'}),
        ])

@app.callback(dash.dependencies.Output('graph-bar-top-n-cust','figure'),
              [dash.dependencies.Input('top-n-cust-sumbit','n_clicks')],
              [dash.dependencies.State('top-n-cust-option','value')]
             )
def update_top_5_cust(n_clicks,input_value):
    #bar_color = ['#f6fbfc', '#eef7fa', '#e6f3f7', '#deeff5', '#d6ebf2', '#cde7f0', '#c5e3ed', '#bddfeb', '#b5dbe8', '#add8e6']
                 
    df = pd.read_excel(data_set,0)
    cust_sales_df = df[['Customer Name','Sales']]
    del df
    cust_sales_pivot = pd.pivot_table(cust_sales_df,index = 'Customer Name', values = 'Sales', aggfunc = 'sum')
    del cust_sales_df 
    cust_sales_flattened_df = pd.DataFrame(cust_sales_pivot.to_records())
    cust_sales_flattened_df.sort_values(by = 'Sales',ascending = False,inplace = True)
    top_n_customers_df = cust_sales_flattened_df[:input_value]
    #print(top_n_customers_df[::-1]['Customer Name'])
    del cust_sales_flattened_df
    data = []
    list_top_n_customers_text = [f'{round(x/1000,2)} K' for x in top_n_customers_df[::-1]['Sales']]
    top_n_customer = go.Bar(x = top_n_customers_df[::-1]['Sales'],
                            y = top_n_customers_df[::-1]['Customer Name'], 
                            orientation = 'h',
                            marker = get_marker(True), 
                            text = list_top_n_customers_text, ##top_n_customers_df[::-1]['Sales'],
                            textposition = 'inside',
                            textfont = get_text_font()
                            )
    data.append(top_n_customer)
    layout = get_graph_layout(graphTitle = f'Top {input_value} Customer by Total Sale',
                              graphWidth = 1400,
                              graphHeight = 1000,
                              graphHoverMode = 'closest',
                              marginLeft = 250,
                              marginRight = 50,
                              marginTop   = 100,
                              marginBottom = 100,
                              graphFontFamily = 'Courier New, monospace',
                              graphFontSize = 20,
                              graphFontColor = '#010c45',
                              xAxisTitle     = "Total Sales in '000",
                              yAxisTitle     = '',
                              axisFontFamily = 'Courier New, monospace',
                              axisFontSize   = 20,
                              axisFontColor  = '#010c45'
                              )
    print(layout)
    return {'data':data,
            'layout':layout
    }

##################
@app.callback(dash.dependencies.Output('graph-bar-cust-sale-by-category','figure'),
              [dash.dependencies.Input('graph-bar-top-n-cust', 'clickData')]
             )
#def sales_by_category(n_clicks,input_value):
def sales_by_category(clickData):
    result = clickData['points']
    df_points = pd.DataFrame(result)
    customer_name = list(df_points['label'])[-1]
    df = pd.read_excel(data_set,0)
    cust_sales_df = df[['Customer Name','Category','Sales']][(df['Customer Name'] == customer_name)]
    del df
    cust_sales_pivot = pd.pivot_table(cust_sales_df,index = 'Category', values = 'Sales', aggfunc = 'sum')
    del cust_sales_df 
    cust_sales_flattened_df = pd.DataFrame(cust_sales_pivot.to_records())
    cust_sales_flattened_df.sort_values(by = 'Sales',ascending = False,inplace = True)

    data = []
    list_sales_by_category =  [ f'{round((x/1000),2)} K' for x in list(cust_sales_flattened_df['Sales'])]
    sales_by_category = go.Bar(x = list(cust_sales_flattened_df['Category']),
                               y = list(cust_sales_flattened_df['Sales']),
                               text = list_sales_by_category,
                               marker = get_marker(True),
                               textposition = 'inside',
                               textfont=get_text_font()
                            )
    data.append(sales_by_category)
    del cust_sales_flattened_df
    layout = get_graph_layout(graphTitle = f'Sales by category for {customer_name}',
                              graphWidth = 800,
                              graphHeight = 1000,
                              graphHoverMode = 'closest',
                              marginLeft = 100,
                              marginRight = 10,
                              marginTop   = 100,
                              marginBottom = 100,
                              graphFontFamily = 'Courier New, monospace',
                              graphFontSize = 20,
                              graphFontColor = '#010c45',
                              xAxisTitle     = 'Item Category',
                              yAxisTitle     = '',
                              axisFontFamily = 'Courier New, monospace',
                              axisFontSize   = 20,
                              axisFontColor  = '#010c45'
                              )
    
   
    return {'data':data,
            'layout':layout
    }   
###################

@app.callback(
    dash.dependencies.Output('hidden-div', 'children'),
    [dash.dependencies.Input('graph-bar-top-n-cust', 'clickData')],
    [dash.dependencies.State('hidden-div', 'children')])
def get_selected_data(clickData, previous):
    if clickData is not None:
        result = clickData['points']
        print(str(pd.Series(pd.DataFrame(result)['label'])))
        if previous:
            previous_list = json.loads(previous)
            if previous_list is not None:
                result = previous_list + result
        return json.dumps(result)

@app.callback(
    Output('selected-data', 'children'),
    [Input('hidden-div', 'children')]
    )
def display_selected_data(points):
    if points:
        result = json.loads(points)
        if result is not None:
            return generate_table(pd.DataFrame(result))
    
if __name__ == '__main__':
    app.run_server()