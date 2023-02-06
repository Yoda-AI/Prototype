from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff

from consts import *

class UniVariable(object):
    def __init__(self, yoda_env, dataframe, app):
        self.yoda_env = yoda_env
        self.dataframe = dataframe
        self.app = app

    def prepare(self):
        RESOLVER = lambda resolver,arg : [resolver[k](*arg) for k in resolver.keys()]

        self.overview_dataframe = pd.DataFrame({  
                                'Name': OVERVIEW_SECTION_RESOLVER.keys(),\
                                'Value': RESOLVER(OVERVIEW_SECTION_RESOLVER,(self.dataframe,))
                            })

        self.columns_dataframes = []
        for column in self.dataframe.columns:
            column_data = { 'Name': list(COLUMN_SECTION_RESOLVER.keys()),
                            'Value': RESOLVER(COLUMN_SECTION_RESOLVER, (self.dataframe, column)) }
            if self.dataframe[column].dtype.name in ['int64','float64']:
                column_data['Name'].extend( COLUMN_SECTION_NUMERIC_RESOLVER.keys() )
                column_data['Value'].extend( RESOLVER(COLUMN_SECTION_NUMERIC_RESOLVER, (self.dataframe, column)) )
                if round(self.dataframe[column].mean(), 2) != 0:
                    column_data['Name'].extend( COLUMN_SECTION_MEAN_NZ_RESOLVER.keys() )
                    column_data['Value'].extend( RESOLVER(COLUMN_SECTION_MEAN_NZ_RESOLVER, (self.dataframe, column)) )
            self.columns_dataframes.append((column, pd.DataFrame(column_data)))
        
        return self

    def get(self):
        return {'overview' : self.overview_dataframe, 'columns': self.columns_dataframes}

    def get_as_html(self):
        elements = []

        elements.append(html.H2(UNIVAR_TITLE, style=TITLE_CSS_PROPS))
        elements.append(html.H2(children=OVERVIEW_SECTION_TITLE))
        elements.append(dbc.Container([dash_table.DataTable(self.overview_dataframe.to_dict('records'), [{"name": i, "id": i} for i in self.overview_dataframe.columns], id='overview', style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'})]))
        elements.append(html.H3(children='Data Table'))
        elements.append(dbc.Container([dash_table.DataTable(self.dataframe.to_dict('records'), [{"name": i, "id": i} for i in self.dataframe.columns], id='datatable-row-ids', page_size=20, filter_action="native", filter_options={"placeholder_text": "Filter column..."}, sort_action="native", sort_mode="multi", column_selectable="single", selected_columns=[], selected_rows=[], page_action="native", page_current=0)]))
        for column, column_dataframe in self.columns_dataframes:
            elements.append(dbc.Container([dash_table.DataTable(
                    column_dataframe.to_dict('records'), [{"name": i, "id": i} for i in column_dataframe.columns], id='col_data_' + column, style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},  style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Name} = "Median Absolute Deviation" && {Value} >=2',
                                'column_id': 'Value'
                            },
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        },
                        {
                            'if': {
                                'filter_query': '({Name} = "Imbalanced (%)" || {Name} = "Outliers (by Z-Score) (%)" || {Name} = "Outliers (by IQR) (%)"|| {Name} = "Outliers (by Modified Z-Score) (%)"|| {Name} = "Outliers (by Winsorization) (%)") && {Value} >5',
                                'column_id': 'Value'
                            },
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        },

                        {
                            'if': {
                                'filter_query': '({Name} = "Skewness" && {Value} >2)|| ( {Name} = "Kurtosis" && {Value} >7)',
                                'column_id': 'Value'
                            },
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        },

                        {
                            'if': {
                                'filter_query': '({Name} = "Zeros (%)" && {Value} >90)',
                                'column_id': 'Value'
                            },
                            'backgroundColor': 'tomato',
                            'color': 'white'
                        }
                    ])]))
            if column in self.yoda_env.numerical.columns:
                fig_hist = px.histogram(self.dataframe, x=column)
                fig_box = px.box(self.dataframe, x=column)
                
                elements.append(html.Div([html.Div([
                    html.Div([dcc.Graph(figure=fig_hist)], className="nine columns"),
                    html.Div([dcc.Graph(figure=fig_box)], className="ten columns")], className="row")]))

            elif column in self.yoda_env.categorical.columns:
                table = pd.DataFrame(self.dataframe[column].value_counts(dropna=False))
                table['index'] = table.index
                elements.append(dbc.Container([dash_table.DataTable(table.to_dict('records'),
                                                                         [{"name": i, "id": i} for i in table.columns],
                                                                         id='datatable-row-ids'+ column,
                                                                         page_size=20, filter_action="native",
                                                                         filter_options={
                                                                             "placeholder_text": "Filter column..."},
                                                                         sort_action="native",
                                                                         sort_mode="multi", column_selectable="single",
                                                                         selected_columns=[], selected_rows=[],
                                                                         page_action="native", page_current=0)]))
                fig_bar = px.bar(table, y=column)
                elements.append(html.Div([html.Div([
                        html.Div([dcc.Graph(figure=fig_bar)], className="nine columns")], className="row")]))
        return elements