from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff

from consts import *

class MultiVariable(object):
    def __init__(self, yoda_env, dataframe, app):
        self.yoda_env = yoda_env
        self.dataframe = dataframe
        self.app = app

    def prepare(self):
        self.df_mask = round(self.yoda_env.numerical.corr(), 2)

        self.heatmap_fig = ff.create_annotated_heatmap(z=self.df_mask.to_numpy(), x=self.df_mask.columns.tolist(), y=self.df_mask.columns.tolist(), colorscale=px.colors.diverging.RdBu, showscale=True, ygap=1, xgap=1)
        self.heatmap_fig.update_xaxes(side="bottom")
        self.heatmap_fig.update_layout(title_text='Heatmap', title_x=0.5, height=1000, xaxis_showgrid=False, yaxis_showgrid=False, xaxis_zeroline=False, yaxis_zeroline=False, yaxis_autorange='reversed', template='seaborn')

        # Fix NaN
        for i in range(len(self.heatmap_fig.layout.annotations)):
            if self.heatmap_fig.layout.annotations[i].text == 'nan':
                self.heatmap_fig.layout.annotations[i].text = ""

        self.fig_parallel_coordinates = px.parallel_coordinates(self.yoda_env.numerical, color=self.yoda_env.target_col)

        return self
    
    def get(self):
        return {}

    def get_as_html(self):
        elements = []
        elements.append(html.H2('Multi-Variables Exploration', style={'textAlign': 'center'}))
        elements.append(dcc.Graph(id='fig_heatmap_2', figure=self.heatmap_fig))

        if self.yoda_env.target_col is not None:
            elements.append(html.Div([dcc.Dropdown(id="dropdown", options=self.yoda_env.numerical.columns.drop(self.yoda_env.target_col), value=self.yoda_env.numerical.columns.drop(self.target_col), multi=True), dcc.Graph(id="graph")]))

            @self.app.callback(Output("graph", "figure"), Input("dropdown", "value"))
            def update_bar_chart(dims):
                return px.scatter_matrix(self.yoda_env.numerical, dimensions=dims, color=self.yoda_env.target_col, height=1500)
        else:
            elements.append(html.Div([dcc.Dropdown(id="dropdown", options=self.yoda_env.numerical.columns, value=self.yoda_env.numerical.columns, multi=True), dcc.Graph(id="graph")]))

            @self.app.callback(Output("graph", "figure"), Input("dropdown", "value"))
            def update_bar_chart(dims):
                return px.scatter_matrix(self.yoda_env.numerical, dimensions=dims, height=1500)

        elements.append(dcc.Graph(id='fig_parallel_coordinates', figure=self.fig_parallel_coordinates))

        return elements