import os
import logging
import secrets
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from pipeline import PropertyPipeline, PropertyValue
from data_sources.csv_data_source import CSVDataSource

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.getLogger().setLevel(LOG_LEVEL)

app = FastAPI(title="Property Price Predictor")
api_key_header = APIKeyHeader(name="X-API-Key")
api_keys = []

train_data_source = CSVDataSource('train.csv')  # or use PostgresDataSource
pipeline = PropertyPipeline(train_data_source)


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key"
    )


@app.post('/create_api_key')
def create_api_key() -> str:
    api_key = secrets.token_hex(12)
    logging.info(f"Created new API key: api_key={api_key}")
    api_keys.append(api_key)

    return api_key


@app.post('/predict')
def predict_property_price(property: PropertyValue, api_key: str = Security(get_api_key)) -> dict:
    logging.info(f"Predicting price for property: {property}")
    prediction = pipeline.predict_property_price(property)
    logging.info(f"Predicted price={prediction}")

    return {'prediction': prediction}
