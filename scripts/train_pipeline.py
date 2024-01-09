from pipeline import PropertyPipeline
from data_sources.csv_data_source import CSVDataSource

PropertyPipeline(CSVDataSource('train.csv'))
