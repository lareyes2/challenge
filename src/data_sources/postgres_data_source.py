import pandas as pd
import psycopg

from data_sources.base_data_source import BaseDataSource


class PostgresDataSource(BaseDataSource):
    query = "SELECT * FROM properties;"

    def __init__(self, postgres_uri):
        self.uri = postgres_uri

    def read(self) -> pd.DataFrame:
        with psycopg.connect(self.uri) as conn:
            with conn.cursor() as cur:
                cur.execute(self.query)
                column_names = [desc.name for desc in cur.description]

                return pd.DataFrame(cur.fetchall(), columns=column_names)

    def __str__(self):
        return f"PostgresDataSource('{self.uri}')"
