# Open Telemetry with Python Demo

## Overview
> This is a simple demo using Python with FastAPI for demonstrating how we can instrument our code to use Open Telemetry. The main purpose is to analyze and trace what happens in the code when we have endpoints and/or API calls.

## Getting started

### Installing the requirements
In the root of the repository,  use this command to install all the necessary dependencies:
```
pip install -r requirements.txt
```

In order to run this demo successfully, they are going to be needed.

### Setting Jaeger
For setting Jaeger (an open source, distributed tracing platform) up, we are going to use a Dockerfile command and then, build it inside of a container:
```
docker run --rm --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.57
```

> [!NOTE]  
> For further details, you may find the full documentation here: https://www.jaegertracing.io/

> Once it is set up, we may export our traces to Jaeger UI and visualize them with plenty of details in this endpoint: `http://localhost:16686/search`.
Notice that the container use several ports, but the 16686 is the one that matters for us.

## Running the API
In order to run the API, and then, send the requests that are going to be analyzed, you must run this command:
```
opentelemetry-instrument --service_name [your_api_name] uvicorn app:app
```
> Note: replace `[your_api_name]` with the service name you want to use. This name is going to be referenced in the traces.

As soon as your API is up, you may make curl requests to the server so as to test the traces.

### Examples

#### Get Home
For instance, to test the `@app.get("/")` endpoint, we may make a request like this:
```
curl http://127.0.0.1:8000/
```

#### Get Item
To test the scenario of `@app.get("/item")`, we must send a curl like this:
```
curl -X GET "http://localhost:8000/item?item_id=1" -H "accept: application/json"
```

#### Call to external API scenario
To test the scenario of a call to an external API (in this example, we are going to use mocked data), you may run this curl:
```
curl -X GET "http://localhost:8000/api" -H "accept: application/json"
```

