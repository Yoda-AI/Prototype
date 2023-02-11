from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff

from consts import *
from .analyzer import Analyzer

class ColumnAnalyzer(Analyzer):
    def __init__(self, yoda_env, dataframe, app, is_sub_analyzer, column):
        super().__init__(yoda_env, dataframe, app, is_sub_analyzer)
        self.column = column
        self.column_dataframe = None

    def prepare(self):
        column_data = { 'Name': list(COLUMN_SECTION_RESOLVER.keys()),
                            'Value': RESOLVER(COLUMN_SECTION_RESOLVER, (self.dataframe, self.column)) }
        if self.dataframe[self.column].dtype.name in ['int64','float64']:
            column_data['Name'].extend( COLUMN_SECTION_NUMERIC_RESOLVER.keys() )
            column_data['Value'].extend( RESOLVER(COLUMN_SECTION_NUMERIC_RESOLVER, (self.dataframe, self.column)) )
            if round(self.dataframe[self.column].mean(), 2) != 0:
                column_data['Name'].extend( COLUMN_SECTION_MEAN_NZ_RESOLVER.keys() )
                column_data['Value'].extend( RESOLVER(COLUMN_SECTION_MEAN_NZ_RESOLVER, (self.dataframe, self.column)) )
        self.column_dataframe = pd.DataFrame(column_data)
        return self

    def get(self):
        return {'column_dataframe': self.column_dataframe}

    def get_as_html(self):
        elements = []

        if_stmnt = lambda x : {'if': {'filter_query': x, 'column_id': 'Value'}, 'backgroundColor': 'tomato', 'color': 'white'}

        elements.append(html.H2("Column - " + self.column, style=TITLE_CSS_PROPS))
        elements.append(dbc.Container([dash_table.DataTable(
                    self.column_dataframe.to_dict('records'), [{"name": i, "id": i} for i in self.column_dataframe.columns], \
                    id='col_data_' + self.column, \
                    style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},  \
                    style_data_conditional=[if_stmnt('{Name} = "Median Absolute Deviation" && {Value} >=2'), \
                    if_stmnt('({Name} = "Imbalanced (%)" || {Name} = "Outliers (by Z-Score) (%)" || {Name} = "Outliers (by IQR) (%)"|| {Name} = "Outliers (by Modified Z-Score) (%)"|| {Name} = "Outliers (by Winsorization) (%)") && {Value} >5'), \
                    if_stmnt('({Name} = "Skewness" && {Value} >2)|| ( {Name} = "Kurtosis" && {Value} >7)'), \
                    if_stmnt('({Name} = "Zeros (%)" && {Value} >90)')], fill_width=True)]))

        if self.column in self.yoda_env.numerical.columns:
            fig_hist = px.histogram(self.dataframe, x=self.column)
            fig_box = px.box(self.dataframe, x=self.column)
            
            elements.append(html.Div([html.Div([
                html.Div([dcc.Graph(figure=fig_hist)], className="nine columns"),
                html.Div([dcc.Graph(figure=fig_box)], className="ten columns")], className="row")]))

        elif self.column in self.yoda_env.categorical.columns:
            table = pd.DataFrame(self.dataframe[self.column].value_counts(dropna=False))
            table['index'] = table.index
            elements.append(dbc.Container([dash_table.DataTable(table.to_dict('records'),
                                                                [{"name": i, "id": i} for i in table.columns],
                                                                id='datatable-row-ids'+ self.column,
                                                                page_size=20, filter_action="native",
                                                                filter_options={
                                                                    "placeholder_text": "Filter column..."},
                                                                sort_action="native",
                                                                sort_mode="multi", column_selectable="single",
                                                                selected_columns=[], selected_rows=[],
                                                                page_action="native", page_current=0, fill_width=True)]))
            fig_bar = px.bar(table, y=self.column)
            elements.append(html.Div([html.Div([
                    html.Div([dcc.Graph(figure=fig_bar)], className="nine columns")], className="row")]))

        return elements

class UniVariable(Analyzer):
    def __init__(self, yoda_env, dataframe, app, is_sub_analyzer):
        super().__init__(yoda_env, dataframe, app, is_sub_analyzer)

    def prepare(self):
        self.overview_dataframe = pd.DataFrame({  
                                'Name': OVERVIEW_SECTION_RESOLVER.keys(),\
                                'Value': RESOLVER(OVERVIEW_SECTION_RESOLVER,(self.dataframe,))
                            })

        for column in self.dataframe.columns:
            sub_app = self._get_sub_app(column)
            sub_analyzer = ColumnAnalyzer(self.yoda_env, self.dataframe, sub_app, True, column).prepare()
            self.sub_analyzers[column] = sub_analyzer
        
        return self

    def get(self):
        return {'overview' : self.overview_dataframe, 'column_analyzers': self.sub_analyzers}

    def get_as_html(self):
        elements = []

        # dcc.Checklist(self.dataframe.to_dict('records')[0].keys(), self.dataframe.to_dict('records')[0].keys(), inline=True)
        elements.append(html.H2(UNIVAR_TITLE, style=TITLE_CSS_PROPS))
        elements.append(html.H2(children=OVERVIEW_SECTION_TITLE, style=TITLE_CSS_PROPS))
        elements.append(dbc.Container([dash_table.DataTable(self.overview_dataframe.to_dict('records'), [{"name": i, "id": i} for i in self.overview_dataframe.columns], id='overview', style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'}, fill_width=True)]))
        elements.append(html.H2(children='Data Table', style=TITLE_CSS_PROPS))
        elements.append(UniVariable.datatable_with_filter(self.dataframe, self.app))

        for key in self.sub_analyzers.keys():
            sub_analyzer = self.sub_analyzers[key]
            elements += sub_analyzer.get_as_html()

        return elements
    
    @staticmethod
    def datatable_with_filter(df, app):
        datatable_columns = [{'label': x, 'value':x} for x in df.to_dict('records')[0].keys()]
        dropdown = dcc.Dropdown(id='filter_columns',options=[{'label': 'All', 'value': 'all'}] + datatable_columns, value='all', multi=True)

        table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='datatable-row-ids', page_size=20, filter_action="native", filter_options={"placeholder_text": "Filter column..."}, sort_action="native", fill_width=False, sort_mode="multi", column_selectable="single", selected_columns=[], selected_rows=[], page_action="native", page_current=0)

        @app.callback(Output(component_id='datatable-row-ids', component_property='columns'),
        [Input(component_id='filter_columns', component_property='value')])
        def update_columns(selected_columns):
            if selected_columns == 'all' or 'all' in selected_columns:
                columns = [{"name": i, "id": i} for i in df.columns]
            else:
                columns = []
                for choice in selected_columns:
                    if choice != 'all':
                        columns += [{"name": choice, "id": choice}]
            return columns
        return dbc.Container([dropdown, table])