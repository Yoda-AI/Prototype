from dash import Dash, html, dcc, Input, Output, dash_table, dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import requests
import plotly.figure_factory as ff


class YodaPrototype:
    def __init__(self, dataframe, overview=True, multi=True, explored_variable=None, target_col=None):
        self.dataframe = dataframe
        self.explored_variable = explored_variable
        self.target_col = target_col
        self.app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
        self.children = [html.H1('Yoda', style={'textAlign': 'center'})]
        self.feedback_sever = "http://192.168.0.208:8888/feedback/"
        if overview:
            self.uni_variable()
        if explored_variable is not None:
            self.bi_variable()
        if multi:
            self.multi_variable()
        self.run()

    def bi_variable(self):

        self.children.append(
            html.H2('Bi-Variables Exploration of ' + self.explored_variable, style={'textAlign': 'center'}))

        funcs = [px.box, px.histogram, px.violin]

        for func in funcs:
            counter = 0
            for i in self.dataframe.columns:
                if i != self.explored_variable:
                    try:
                        fig = func(self.dataframe, x=self.explored_variable, y=i, color=self.target_col,
                                   title=f"{func.__name__} {self.explored_variable} and {i}")
                        self.children.append(dcc.Graph(
                            id='fig_' + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable),
                            figure=fig))
                        self.children.append(dbc.Button("Valuable",
                                                        id='valuable_' + str(func.__name__) + str(counter) + str(
                                                            i) + str(self.explored_variable),
                                                        color="primary"))
                        self.children.append(html.Span(
                            id="example_1 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable)))

                        @self.app.callback(Output(
                            "example_1 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable),
                            "children"),
                                           [Input('valuable_' + str(func.__name__) + str(counter) + str(i) + str(
                                               self.explored_variable), "id")])
                        def on_button_click(n):
                            requests.request(url=self.feedback_sever + n, method='Get')

                        self.children.append(dbc.Button("New to me",
                                                        id='new_' + str(func.__name__) + str(counter) + str(i) + str(
                                                            self.explored_variable), color="primary"))
                        self.children.append(html.Span(
                            id="example_2 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable)))

                        @self.app.callback(Output(
                            "example_2 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable),
                            "children"),
                                           [Input('new_' + str(func.__name__) + str(counter) + str(i) + str(
                                               self.explored_variable), "id")])
                        def on_button_click(n):
                            requests.request(url=self.feedback_sever + n, method='Get')

                        self.children.append(dbc.Button("Not useful",
                                                        id='no_' + str(func.__name__) + str(counter) + str(i) + str(
                                                            self.explored_variable), color="primary"))
                        self.children.append(html.Span(
                            id="example_3 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable)))

                        @self.app.callback(Output(
                            "example_3 " + str(func.__name__) + str(counter) + str(i) + str(self.explored_variable),
                            "children"),
                                           [Input('no_' + str(func.__name__) + str(counter) + str(i) + str(
                                               self.explored_variable), "id")])
                        def on_button_click(n):
                            requests.request(url=self.feedback_sever + n, method='Get')

                        counter += 1
                    except:
                        requests.request(
                            url=self.feedback_sever + f"Error with {func.__name__} {i} and {self.explored_variable}",
                            method='Get')

    def multi_variable(self):
        self.correlation_heatmap()

        if self.target_col is not None:
            self.children.append(
                html.Div([dcc.Dropdown(id="dropdown", options=self.dataframe.columns.drop(self.target_col),
                                       value=self.dataframe.columns.drop(self.target_col), multi=True),
                          dcc.Graph(id="graph")]))

            @self.app.callback(Output("graph", "figure"), Input("dropdown", "value"))
            def update_bar_chart(dims):
                fig = px.scatter_matrix(self.dataframe, dimensions=dims, color=self.target_col, height=1500)
                return fig
        else:
            self.children.append(html.Div(
                [dcc.Dropdown(id="dropdown", options=self.dataframe.columns, value=self.dataframe.columns, multi=True),
                 dcc.Graph(id="graph")]))

            @self.app.callback(Output("graph", "figure"), Input("dropdown", "value"))
            def update_bar_chart(dims):
                fig = px.scatter_matrix(self.dataframe, dimensions=dims, height=1500)
                return fig
        self.parallel_coordinates()

    def uni_variable(self):
        self.children.append(html.H2('Uni-Variables Exploration', style={'textAlign': 'center'}))

        self.children.append(html.H2(children='Overview'))
        overview = {'Name': ['Number of variables', 'Number of observations', 'Missing cells', 'Missing cells (%)',
                             'Duplicate rows', 'Duplicate rows (%)'],
                    'Value': [self.dataframe.shape[1],
                              self.dataframe.shape[0],
                              self.dataframe.isnull().sum().sum(),
                              round(self.dataframe.isnull().sum().sum() / (
                                          self.dataframe.shape[0] * self.dataframe.shape[1]), 2),
                              self.dataframe.duplicated().sum(),
                              round(self.dataframe.duplicated().sum() / self.dataframe.shape[0], 2)
                              ]}
        overview = pd.self.dataframe(overview)
        self.children.append(dbc.Container([dash_table.DataTable(
            overview.to_dict('records'), [{"name": i, "id": i} for i in overview.columns], id='overview',
            style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
        )]))
        self.children.append(html.H3(children='Data Table'))
        self.children.append(dbc.Container([

            dash_table.DataTable(self.dataframe.to_dict('records'),
                                 [{"name": i, "id": i} for i in self.dataframe.columns], id='datatable-row-ids',
                                 page_size=20, filter_action="native",
                                 filter_options={"placeholder_text": "Filter column..."}, sort_action="native",
                                 sort_mode="multi", column_selectable="single",
                                 selected_columns=[], selected_rows=[], page_action="native", page_current=0)]))

        for col in self.dataframe.columns:
            self.children.append(html.H3(children=""
                                                  "" + col))
            col_data = {'Name': ['Data Type', 'Number of unique values', 'Unique values (%)',
                                 'Number of missing values', 'Missing values (%)'],
                        'Value': [self.dataframe[col].dtype.name, len(self.dataframe[col].unique()),
                                  round((len(self.dataframe[col].unique()) / len(self.dataframe)) * 100, 2),
                                  self.dataframe[col].isnull().sum(),
                                  round((self.dataframe[col].isnull().sum() / len(self.dataframe)) * 100, 2)
                                  ]}
            if self.dataframe[col].dtype.name == 'int64' or self.dataframe[col].dtype.name == 'float64':
                col_data['Name'].extend(
                    ['Mean', 'Median', 'Standard Deviation', 'Minimum', 'Maximum', 'Range', 'Variance', 'Skewness',
                     'Kurtosis',
                     'Monotonicity (increasing)', 'Monotonicity (decreasing)', 'Median Absolute Deviation',
                     'Coefficient of Variation', 'Interquartile Range (IQR)', 'Interquartile Range (IQR) (%)',
                     'Quantile 0.25', 'Quantile 0.75', '5th Percentile', '95th Percentile', 'Number of zeros',
                     'Zeros (%)', 'Imbalanced', 'Imbalanced (%)',
                     'Number of negative values', 'Negative values (%)', 'Number of positive values',
                     'Positive values (%)',
                     'Number of outliers (by IQR)', 'Outliers (by IQR) (%)', 'Number of outliers (by Z-Score)',
                     'Outliers (by Z-Score) (%)',
                     'Number of outliers (by Modified Z-Score)', 'Outliers (by Modified Z-Score) (%)',
                     'Number of outliers (by Winsorization)',
                     'Outliers (by Winsorization) (%)', "high correlation", "low correlation"])
                col_data['Value'].extend([round(self.dataframe[col].mean(), 2), self.dataframe[col].median(),
                                          round(self.dataframe[col].std(), 2), self.dataframe[col].min(),
                                          self.dataframe[col].max()
                                             , round(self.dataframe[col].max() - self.dataframe[col].min(), 2),
                                          round(self.dataframe[col].var(), 2),
                                          round(self.dataframe[col].skew(), 2), round(self.dataframe[col].kurt(), 2),
                                          self.dataframe[col].is_monotonic_increasing,
                                          self.dataframe[col].is_monotonic_decreasing,
                                          round((self.dataframe[col] - self.dataframe[col].mean()).abs().mean(), 2),
                                          round(self.dataframe[col].std() / self.dataframe[col].mean(), 2),
                                          self.dataframe[col].quantile(0.75) - self.dataframe[col].quantile(0.25),
                                          round(((self.dataframe[col].quantile(0.75) - self.dataframe[col].quantile(
                                              0.25)) / self.dataframe[col].mean()) * 100, 2),
                                          self.dataframe[col].quantile(0.25), self.dataframe[col].quantile(0.75),
                                          self.dataframe[col].quantile(0.05), self.dataframe[col].quantile(0.95),
                                          (self.dataframe[col] == 0).sum(),
                                          round(((self.dataframe[col] == 0).sum() / len(self.dataframe)) * 100, 2),
                                          round((self.dataframe[col].value_counts().max() / self.dataframe[
                                              col].value_counts().min()), 2),
                                          round(((self.dataframe[col].value_counts().max() / self.dataframe[
                                              col].value_counts().min()) / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] < 0).sum(),
                                          round(((self.dataframe[col] < 0).sum() / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] > 0).sum(),
                                          round(((self.dataframe[col] > 0).sum() / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] < self.dataframe[col].quantile(0.25) - 1.5 * (
                                                      self.dataframe[col].quantile(0.75) - self.dataframe[col].quantile(
                                                  0.25))).sum(),
                                          round(((self.dataframe[col] < self.dataframe[col].quantile(0.25) - 1.5 * (
                                                      self.dataframe[col].quantile(0.75) - self.dataframe[col].quantile(
                                                  0.25))).sum() / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] < self.dataframe[col].mean() - 3 * self.dataframe[
                                              col].std()).sum(),
                                          round(((self.dataframe[col] < self.dataframe[col].mean() - 3 * self.dataframe[
                                              col].std()).sum() / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] < self.dataframe[col].mean() - 1.4826 * (
                                                      self.dataframe[col] - self.dataframe[
                                                  col].median()).abs().median()).sum(),
                                          round(((self.dataframe[col] < self.dataframe[col].mean() - 1.4826 * (
                                                      self.dataframe[col] - self.dataframe[
                                                  col].median()).abs().median()).sum() / len(self.dataframe)) * 100, 2),
                                          (self.dataframe[col] < self.dataframe[col].quantile(0.05)).sum(),
                                          round(((self.dataframe[col] < self.dataframe[col].quantile(0.05)).sum() / len(
                                              self.dataframe)) * 100, 2),
                                          str(self.dataframe.corr()[col].sort_values(ascending=False)[
                                              1:5].to_dict()),
                                          str(self.dataframe.corr()[col].sort_values(ascending=False)[-5:].to_dict())
                                          ])
            col_data = pd.self.dataframe(col_data)
            self.children.append(dbc.Container([dash_table.DataTable(
                col_data.to_dict('records'), [{"name": i, "id": i} for i in col_data.columns], id='col_data_' + col,
                style_cell={'textAlign': 'left', 'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Name} = "Standard Deviation" && {Value} >2',
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
                    }
                ])]))
            fig_hist = px.histogram(self.dataframe, x=col)
            fig_box = px.box(self.dataframe, x=col)
            self.children.append(html.Div([html.Div([
                html.Div([dcc.Graph(figure=fig_hist)], className="nine columns"),
                html.Div([dcc.Graph(figure=fig_box)], className="ten columns")], className="row")]))

    def correlation_heatmap(self):
        self.children.append(html.H2('Multi-Variables Exploration', style={'textAlign': 'center'}))
        df_mask = round(self.dataframe.corr(), 2)
        fig = ff.create_annotated_heatmap(z=df_mask.to_numpy(), x=df_mask.columns.tolist(), y=df_mask.columns.tolist(),
                                          colorscale=px.colors.diverging.RdBu, hoverinfo="none", showscale=True, ygap=1,
                                          xgap=1)
        fig.update_xaxes(side="bottom")
        fig.update_layout(title_text='Heatmap', title_x=0.5, height=1000, xaxis_showgrid=False, yaxis_showgrid=False,
                          xaxis_zeroline=False, yaxis_zeroline=False, yaxis_autorange='reversed', template='seaborn')
        for i in range(len(fig.layout.annotations)):
            if fig.layout.annotations[i].text == 'nan':
                fig.layout.annotations[i].text = ""
        self.children.append(dcc.Graph(id='fig_heatmap_2', figure=fig))

    def parallel_coordinates(self):
        fig = px.parallel_coordinates(self.dataframe, color=self.target_col)
        self.children.append(dcc.Graph(id='fig_parallel_coordinates', figure=fig))

    def run(self):

        self.app.layout = html.Div(children=self.children)

        if __name__ == '__main__':
            self.app.run_server(debug=False, host='0.0.0.0')
