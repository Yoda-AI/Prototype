from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import requests
import plotly.figure_factory as ff
import threading

from consts import *
from mutators.DateMutator import DateMutator

from analyzers.univariable import UniVariable
from analyzers.bivariable import BiVariable
from analyzers.multivariable import MultiVariable
from formatters.dataformatter import DataFormatter

class Yoda:
    def __init__(self, dataframe, overview=True, multi=True, explored_variable=None, target_col=None):
        self.dataframe = Yoda._mutate_dataframe(dataframe)
        self.explored_variable = explored_variable
        self.target_col = target_col
        self.overview = overview
        self.multi = multi

        self.init_logs_server()
        self.init_webapp()
        self.init_special_fields()
        self.init_analyzers()
        
    def init_logs_server(self):
        self.feedback_sever = "http://77.125.86.248:8888/feedback/"

    def init_webapp(self):
        self.app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

    def init_analyzers(self):
        self.analyzers = {}
        if self.overview:
            self.analyzers['Uni'] = {'analyzer':UniVariable,'result':None}
        if self.explored_variable is not None:
            self.analyzers['Bi'] = {'analyzer':BiVariable,'result':None}
        if self.multi:
            self.analyzers['Multi'] = {'analyzer':MultiVariable,'result':None}

    def init_special_fields(self):
        self.categorical = self.dataframe[self.dataframe.select_dtypes(include = ["object"]).keys()]
        self.numerical = self.dataframe[self.dataframe.select_dtypes(include = ["int64","float64"]).keys()]

    @staticmethod
    def _mutate_dataframe(dataframe):
        mutators = [DateMutator]
        for mutator in mutators:
            dataframe = mutator(dataframe).get()
        return dataframe

    def prepare(self):
        for analyzer_name in self.analyzers.keys():
            analyzer = self.analyzers[analyzer_name]['analyzer'](self, self.dataframe).prepare()
            self.analyzers[analyzer_name]['result'] = analyzer
        return self

    def get_analysis_raw(self):
        result = {}
        for analyzer_name in self.analyzers.keys():
            result[analyzer_name] = self.analyzers[analyzer_name]['result'].get()

        return result

    def run_webserver(self, is_async=False):
        elements = [html.H1('Yoda', style={'textAlign': 'center'})]
        for analyzer_name in self.analyzers.keys():
            html_elements = DataFormatter(self.analyzers[analyzer_name]['result']).get_as_html()
            elements = elements + html_elements
        self.app.layout = html.Div(children=elements)

        if is_async:
            server = threading.Thread(target=self._run_server, args=())
            server.start()
        else:
            while True:
                self._run_server()

    def _run_server(self):
        while True:
            self.app.run_server(debug=True)