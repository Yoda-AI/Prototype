from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import requests
import plotly.figure_factory as ff
import threading

from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

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
        self.app_flask = Flask(__name__)
        self.total_app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL], server=self.app_flask, url_base_pathname='/dashboard/')

        self.app_main = DispatcherMiddleware(self.app_flask, {})

        self.init_webserver_ui()

    def init_webserver_ui(self):
        @self.app_flask.route('/')
        def main():
            return render_template('index.html')

        # Used in flask template.
        @self.app_flask.context_processor
        def get_analyzers():
            return {'analyzers': self.analyzers}

    def init_analyzers(self):
        self.analyzers = {}
        if self.overview:
            app_uni = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL], server=self.app_flask, url_base_pathname='/dashboard/Uni/')
            self.analyzers['Uni'] = {'analyzer':UniVariable,'result':None,'app':app_uni}
        if self.explored_variable is not None:
            app_bi = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL], server=self.app_flask, url_base_pathname='/dashboard/Bi/')
            self.analyzers['Bi'] = {'analyzer':BiVariable,'result':None,'app':app_bi}
        if self.multi:
            app_multi = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL], server=self.app_flask, url_base_pathname='/dashboard/Multi/')
            self.analyzers['Multi'] = {'analyzer':MultiVariable,'result':None,'app':app_multi}

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
        new_analyzers = {}
        for analyzer_name in self.analyzers.keys():
            analyzer = self.analyzers[analyzer_name]['analyzer'](self, self.dataframe, self.analyzers[analyzer_name]['app'], False).prepare()
            self.analyzers[analyzer_name]['result'] = analyzer
            
            if len(analyzer.sub_analyzers.keys()) > 0:
                for key in analyzer.sub_analyzers:
                    new_analyzer = analyzer.sub_analyzers[key]
                    new_analyzers[f'{analyzer_name}/{key}/'] = {'analyzer':type(new_analyzer),'result':new_analyzer,'app':new_analyzer.app}
        self.analyzers.update(new_analyzers)

        return self

    def get_analysis_raw(self):
        result = {}
        for analyzer_name in self.analyzers.keys():
            result[analyzer_name] = self.analyzers[analyzer_name]['result'].get()

        return result

    def run_webserver(self, is_async=False):
        total_elements = [html.H1('Yoda', style={'textAlign': 'center'})]
        for analyzer_name in self.analyzers.keys():
            html_elements = DataFormatter(self.analyzers[analyzer_name]['result']).get_as_html()
            self.analyzers[analyzer_name]['app'].layout = html.Div(children=html_elements)
            if not self.analyzers[analyzer_name]['result'].is_sub_analyzer:
                total_elements = total_elements + html_elements
        self.total_app.layout = html.Div(children=total_elements)

        if is_async:
            server = threading.Thread(target=self._run_server, args=())
            server.start()
        else:
            while True:
                self._run_server()

    def _run_server(self):
        run_simple('0.0.0.0', 8050, self.app_main, use_reloader=True, use_debugger=True, threaded=True)