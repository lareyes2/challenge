import pandas as pd

from data_sources.base_data_source import BaseDataSource


class CSVDataSource(BaseDataSource):
    def __init__(self, path):
        self.path = path

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    def __str__(self):
        return f"CSVDataSource('{self.path}')"
