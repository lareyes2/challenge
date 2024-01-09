import pandas as pd
import joblib
import logging
from typing import Literal
from pydantic import BaseModel
from pydantic.types import PositiveInt, PositiveFloat
from category_encoders import TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor

from data_sources.base_data_source import BaseDataSource


class PropertyValue(BaseModel):
    type: Literal['casa', 'departamento']
    sector: str
    net_usable_area: PositiveFloat
    net_area: PositiveFloat
    n_rooms: PositiveInt
    n_bathroom: PositiveInt
    latitude: float
    longitude: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "casa",
                    "sector": "las condes",
                    "net_usable_area": 132,
                    "net_area": 267,
                    "n_rooms": 4,
                    "n_bathroom": 2,
                    "latitude": -33.4237,
                    "longitude": -70.6099
                }
            ]
        }
    }


class PropertyPipeline:
    pipeline_path = "property_pipeline.pkl"
    categorical_cols = ["type", "sector"]
    target_column = "price"

    def __init__(self, data_source: BaseDataSource):
        try:
            self.pipeline = joblib.load(self.pipeline_path)
        except Exception as e:
            logging.warning(
                f"Failed to load pipeline on '{self.pipeline_path}': {str(e)}"
            )
            self.pipeline = self._create_pipeline()
            self._train_pipeline(data_source)
            joblib.dump(self.pipeline, self.pipeline_path)
            logging.info("Dumped pipeline on {pipeline_path}")

    def _create_pipeline(self) -> Pipeline:
        categorical_transformer = TargetEncoder()
        preprocessor = ColumnTransformer(
            transformers=[
                ('categorical', categorical_transformer, self.categorical_cols)
            ]
        )
        steps = [
            ('preprocessor', preprocessor),
            ('model', GradientBoostingRegressor(**{
                "learning_rate": 0.01,
                "n_estimators": 300,
                "max_depth": 5,
                "loss": "absolute_error"
            }))
        ]

        return Pipeline(steps)

    def _train_pipeline(self, data_source: BaseDataSource):
        logging.info(f"Training pipeline with data on {data_source}.")
        try:
            train_data = data_source.read()
            self.pipeline.fit(
                train_data.drop(columns=[self.target_column]),
                train_data[self.target_column]
            )
        except Exception as e:
            logging.exception(
                f"Failed to training pipeline make sure the training data is available: {str(e)}")

    def predict_property_price(self, property: PropertyValue) -> float:
        data_in = pd.DataFrame([property.model_dump()])
        prediction = self.pipeline.predict(data_in)

        return prediction[0]
