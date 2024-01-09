# Property Price Predictor

Ready to deploy property price predictor pipeline using scikit-learn and FastAPI. 
## Folder structure
- scripts
  - train_pipeline.py: is a script used for train the model(generates the .pkl).
- src
  - app.py: it contains the endpoints definition of the API.
  - pipeline.py: Is the code with the definition of the class that create the model property pipeline.
- requirements.txt: contains all the dependencies required to run the solution.
- Dockerfile: it contains the instruction to generate the image.
- .gitignore: is a list of the files that can't be uploaded to the public github repository.
- .dockerignore: is for not uploading unwanted files or directories to docker image.

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

* The input only takes CSV, for using another input like Postgres Database you need change line 17 in app.py for PostgresDataSource.
* The security of the API Token need improvement. Because there is no need for credentials to generate an API Key(You can create multiples). For fix this you will need to develop all the login logic. (I asummed that was out of scope)
* A github Action could be created to automate the docker build process and upload the resulting image to registry (for automate deployment). And the image can be use for the pipeline in the Cloud provider.
* The commit history of the repository doesnt exist because I made everything local and forget to upload :S, but the process was: 1) Creation of the API 2) Implementing the model (adapting the jupyter notebook) 3) Add the validation and security with API Key 4) Create Docker file.
* The solution can be more decouple, the training process is to implicit(start with looking for the .pkl file) in case you use another model for example a more complex one that required more resources, I think it will be difficult to manage (I feel like will be having problems scaling with others models).


