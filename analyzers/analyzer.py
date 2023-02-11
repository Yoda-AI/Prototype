from dash import dash
import dash_bootstrap_components as dbc

from consts import *

class Analyzer(object):
    def __init__(self, yoda_env, dataframe, app, is_sub_analyzer):
        self.yoda_env = yoda_env
        self.dataframe = dataframe
        self.app = app
        self.sub_analyzers = {}
        self.is_sub_analyzer = is_sub_analyzer

    def prepare(self):
        return self

    def get(self):
        return {}

    def get_as_html(self):
        elements = []
        return elements

    def _get_sub_app(self, name):
        return dash.Dash(external_stylesheets=[dbc.themes.JOURNAL], server=self.yoda_env.app_flask, url_base_pathname=f"{self.app.config['url_base_pathname']}{name}/")