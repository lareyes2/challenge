FROM python:3.12 as trainer
# Build command: docker build . --tag property_predictor --build-arg="TRAINIG_DATA_CSV=./train.csv"
# Run command: docker run -p 80:80 -t property_predictor

WORKDIR /app

# Where to search for the training data csv
ARG TRAINIG_DATA_CSV=train.csv

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy source code
COPY ./src .

# Generate pipeline and train with CSV file
COPY ${TRAINIG_DATA_CSV} .
COPY ./scripts/train_pipeline.py .
RUN python train_pipeline.py

FROM python:3.12

ENV LOG_LEVEL=WARNING
WORKDIR /app

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy source code
COPY ./src .

# Copy pipeline
COPY --from=trainer /app/property_pipeline.pkl .

# Run API server
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
