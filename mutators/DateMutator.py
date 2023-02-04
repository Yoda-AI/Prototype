from .DataframeMutator import DataframeMutator

class DateMutator(DataframeMutator):
    def analyze(self):
        for col in self.dataframe.columns:
            try:
                self.dataframe[col] = pd.to_datetime(self.dataframe[col], utc=True)
                self.dataframe[col + ' year'] = self.dataframe[col].dt.year
                self.dataframe[col + ' month'] = self.dataframe[col].dt.month
                self.dataframe[col + ' day'] = self.dataframe[col].dt.day
                self.dataframe[col + ' hour'] = self.dataframe[col].dt.hour
            except:
                pass