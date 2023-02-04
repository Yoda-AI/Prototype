from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import requests

class BiVariable(object):
    def __init__(self, yoda_env, dataframe):
        self.yoda_env = yoda_env
        self.dataframe = dataframe

    def prepare(self):
        self.func_graphs = []

        funcs = [px.box, px.histogram, px.violin]

        for func in funcs:
            counter = 0
            for column in self.dataframe.columns:
                if column != self.explored_variable:
                    fig = func(self.dataframe, x=self.yoda_env.explored_variable, y=column, color=self.target_col, title=f"{func.__name__} {self.yoda_env.explored_variable} and {column}")
                    self.func_graphs.append({'fig' : fig, 'counter:' : counter, 'func' : func, 'column':column})
                counter += 1

        return self
    
    def get(self):
        return {'figs' : self.func_graphs}
    
    def get_as_html(self):
        elements = []

        elements.append(html.H2('Bi-Variables Exploration of ' + self.yoda_env.explored_variable, style={'textAlign': 'center'}))

        for func_graph in self.func_graphs:
            elements.append(dcc.Graph(id='fig_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), figure=func_graph['fig']))
            elements.append(html.Span(id="example_1 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable)))
            @self.yoda_env.app.callback(Output("example_1 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), "children"),[Input('valuable_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), "id")])
            def on_button_click(n):
                requests.request(url=self.yoda_env.feedback_sever + n, method='Get')
            
            elements.append(dbc.Button("New to me", id='new_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), color="primary"))
            elements.append(html.Span(id="example_2 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable)))
            @self.yoda_env.app.callback(Output("example_2 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), "children"), [Input('new_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), "id")])
            def on_button_click(n):
                requests.request(url=self.feedback_sever + n, method='Get')

            elements.append(dbc.Button("Not useful",id='no_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), color="primary"))
            elements.append(html.Span(id="example_3 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable)))
            @self.app.callback(Output("example_3 " + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable),"children"),[Input('no_' + str(func_graph['func'].__name__) + str(func_graph['counter']) + str(func_graph['column']) + str(self.yoda_env.explored_variable), "id")])
            def on_button_click(n):
                requests.request(url=self.feedback_sever + n, method='Get')
        return elements