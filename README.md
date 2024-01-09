# Property Price Predictor

Ready to deploy property price predictor pipeline using scikit-learn and FastAPI.

## How to run

To run locally have a training data CSV `train.csv` on `src` folder and execute the following commands:

```unix
pip install -r ./requirements.txt
cd src
uvicorn app:app --reload
```

Or have the CSV on project folder and use the `Dockerfile`.

## How to test API

The API docs can be viewed and tested on the `/docs` path.

Or you can test them using `curl`:

```unix
curl -X 'POST' 'localhost/create_api_key'
curl -X POST 'localhost/predict' \
 -H 'X-API-Key: {returned_api_key}' \
 -H 'Content-Type: application/json' \
 -d '{"type":"casa","sector":"las condes","net_usable_area":170,"net_area":300,"n_rooms":4,"n_bathroom":3,"latitude":-33.4129,"longitude":-70.571}'
```

## Assumptions and suggested improvements

* 
