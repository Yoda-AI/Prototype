# UniVariable
UNIVAR_TITLE = 'Uni-Variables Exploration'

OVERVIEW_SECTION_TITLE = "Overview"
OVERVIEW_SECTION_RESOLVER = { 'Number of variables' : lambda dataframe : dataframe.shape[1], \
                            'Number of observations' : lambda dataframe : dataframe.shape[0], \
                            'Missing cells' : lambda dataframe : dataframe.isnull().sum().sum(), \
                            'Missing cells (%)' : lambda dataframe : round(dataframe.isnull().sum().sum() / (dataframe.shape[0] * dataframe.shape[1]), 2), \
                            'Duplicate rows' : lambda dataframe : dataframe.duplicated().sum(), \
                            'Duplicate rows (%)' : lambda dataframe : round(dataframe.duplicated().sum() / dataframe.shape[0], 2),
                            }

COLUMN_SECTION_TITLE = "Column: %s"
COLUMN_SECTION_RESOLVER = { 'Data Type' : lambda dataframe, col : dataframe[col].dtype.name, \
                            'Number of unique values' : lambda dataframe, col : len(dataframe[col].unique()), \
                            'Unique values (%)' : lambda dataframe, col : round((len(dataframe[col].unique()) / len(dataframe)) * 100, 2), \
                            'Number of missing values' : lambda dataframe, col : dataframe[col].isnull().sum(), \
                            'Missing values (%)' : lambda dataframe, col : round((dataframe[col].isnull().sum() / len(dataframe)) * 100, 2), \
                        }
COLUMN_SECTION_NUMERIC_RESOLVER = {
                                    'Mean' : lambda dataframe, col : round(dataframe[col].mean(), 2), \
                                    'Median' : lambda dataframe, col : dataframe[col].median(), \
                                    'Standard Deviation' : lambda dataframe, col : round(dataframe[col].std(), 2), \
                                    'Minimum' : lambda dataframe, col : dataframe[col].min(), \
                                    'Maximum' : lambda dataframe, col : dataframe[col].max(), \
                                    'Range' : lambda dataframe, col : round(dataframe[col].max() - dataframe[col].min(), 2), \
                                    'Variance' : lambda dataframe, col : round(dataframe[col].var(), 2), \
                                    'Skewness' : lambda dataframe, col : round(dataframe[col].skew(), 2), \
                                    'Kurtosis' : lambda dataframe, col : round(dataframe[col].kurt(), 2), \
                                    'Monotonicity (increasing)' : lambda dataframe, col : dataframe[col].is_monotonic_increasing, \
                                    'Monotonicity (decreasing)' : lambda dataframe, col : dataframe[col].is_monotonic_decreasing, \
                                    'Median Absolute Deviation' : lambda dataframe, col : round((dataframe[col] - dataframe[col].mean()).abs().mean(), 2), \
                                    'Interquartile Range (IQR)' : lambda dataframe, col : dataframe[col].quantile(0.75) - dataframe[col].quantile(0.25), \
                                    'Quantile 0.25' : lambda dataframe, col :dataframe[col].quantile(0.25), \
                                    'Quantile 0.75' : lambda dataframe, col : dataframe[col].quantile(0.75), \
                                    '5th Percentile' : lambda dataframe, col : dataframe[col].quantile(0.05), \
                                    '95th Percentile' : lambda dataframe, col : dataframe[col].quantile(0.95), \
                                    'Number of zeros' : lambda dataframe, col : (dataframe[col] == 0).sum(), \
                                    'Zeros (%)' : lambda dataframe, col : round(((dataframe[col] == 0).sum() / len(dataframe)) * 100, 2), \
                                    'Imbalanced' : lambda dataframe, col : round((dataframe[col].value_counts().max() / dataframe[col].value_counts().min()), 2), \
                                    'Imbalanced (%)' : lambda dataframe, col : round(((dataframe[col].value_counts().max() / dataframe[col].value_counts().min()) / len(dataframe)) * 100, 2), \
                                    'Number of negative values' : lambda dataframe, col : (dataframe[col] < 0).sum(), \
                                    'Negative values (%)' : lambda dataframe, col : round(((dataframe[col] < 0).sum() / len(dataframe)) * 100, 2), \
                                    'Number of positive values' : lambda dataframe, col : (dataframe[col] > 0).sum(), \
                                    'Positive values (%)' : lambda dataframe, col : round(((dataframe[col] > 0).sum() / len(dataframe)) * 100, 2), \
                                    'Number of outliers (by IQR)' : lambda dataframe, col : (dataframe[col] < dataframe[col].quantile(0.25) - 1.5 * (dataframe[col].quantile(0.75) - dataframe[col].quantile(0.25))).sum(), \
                                    'Outliers (by IQR) (%)' : lambda dataframe, col : round(((dataframe[col] < dataframe[col].quantile(0.25) - 1.5 * (dataframe[col].quantile(0.75) - dataframe[col].quantile(0.25))).sum() / len(dataframe)) * 100, 2), \
                                    'Number of outliers (by Z-Score)' : lambda dataframe, col : (dataframe[col] < dataframe[col].mean() - 3 * dataframe[col].std()).sum(), \
                                    'Outliers (by Z-Score) (%)' : lambda dataframe, col : round(((dataframe[col] < dataframe[col].mean() - 3 * dataframe[col].std()).sum() / len(dataframe)) * 100, 2), \
                                    'Number of outliers (by Modified Z-Score)' : lambda dataframe, col : (dataframe[col] < dataframe[col].mean() - 1.4826 * (dataframe[col] - dataframe[col].median()).abs().median()).sum(), \
                                    'Outliers (by Modified Z-Score) (%)' : lambda dataframe, col : round(((dataframe[col] < dataframe[col].mean() - 1.4826 * (dataframe[col] - dataframe[col].median()).abs().median()).sum() / len(dataframe)) * 100, 2), \
                                    'Number of outliers (by Winsorization)' : lambda dataframe, col : (dataframe[col] < dataframe[col].quantile(0.05)).sum(), \
                                    'Outliers (by Winsorization) (%)' : lambda dataframe, col : round(((dataframe[col] < dataframe[col].quantile(0.05)).sum() / len(dataframe)) * 100, 2), \
                                    'high correlation' : lambda dataframe, col : str(dataframe.corr()[col].sort_values(ascending=False)[1:5].to_dict()), \
                                    'low correlation' : lambda dataframe, col : str(dataframe.corr()[col].sort_values(ascending=False)[-5:].to_dict()),  \
                                    }

COLUMN_SECTION_MEAN_NZ_RESOLVER = {
                                        'Coefficient of Variation' : lambda dataframe, col : round(round(dataframe[col].std(),2) / round(dataframe[col].mean(), 2),2),\
                                        'Interquartile Range (IQR) (%)' : lambda dataframe, col : round(((dataframe[col].quantile(0.75) - dataframe[col].quantile(0.25)) / dataframe[col].mean()) * 100, 2) ,
                                    }

# Html
TITLE_CSS_PROPS = {'textAlign': 'center'}



RESOLVER = lambda resolver,arg : [resolver[k](*arg) for k in resolver.keys()]