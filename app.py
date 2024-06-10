import time
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
import requests

# Initialize OTEL
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
# Done initializing OTEL

app = FastAPI()

@app.get("/")
def get_homepage():
    count = 1
    while count <= 3:
        with tracer.start_as_current_span(f"loop-count-{count}") as span:
            count += 1
            time.sleep(1)

    return {
        "status": "OK",
        "foo": "bar"
    }

@app.get("/item")
async def process_item(item_id: int):
    with tracer.start_as_current_span("process_item") as span:
        span.set_attribute("item_id", item_id)
        span.add_event("Processing started")
        if item_id % 2 == 0:
            span.add_event("Even item detected")
        else:
            span.add_event("Odd item detected")
        
        time.sleep(2)
        
        span.add_event("Processing completed")
        return {"status": "processed", "item_id": item_id}

@app.get("/error")
async def generate_error():
    with tracer.start_as_current_span("generate_error") as span:
        try:
            raise ValueError("This is a test error")
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/api")
async def call_external_api():
    with tracer.start_as_current_span("call_external_api") as span:
        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = requests.get(url)
        span.set_attribute("http.status_code", response.status_code)
        span.set_attribute("http.url", url)
        span.add_event("External API called")
        
        if response.status_code == 200:
            span.add_event("Successful response")
            return response.json()
        else:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Failed to call external API"))
            return {"error": "Failed to fetch data"}