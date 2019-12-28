# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 05:29:23 2019

@author: Home-PC
"""

import dash
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash()
#app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.title = 'Global Super Store'


app.layout = html.Div([
                html.Div([
                        html.H1(children = 'Banner')
                        ],className="row"),
                html.Div([
                        html.Div([
                                html.H2('Section 2.1'),
                                dcc.Graph()
                                ],className = 'six columns'),
                        html.Div([
                                html.H2('Section 2.2'),
                                dcc.Graph()
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
                        ],className="row")
        ])

if __name__ == '__main__':
    app.run_server()