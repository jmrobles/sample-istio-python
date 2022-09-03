import logging
from functools import wraps
from fastapi import FastAPI, Request
import time
import random

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry import propagate


logger = logging.getLogger(__name__)
# Set B3 headers format
propagate.set_global_textmap(B3MultiFormat())


jaeger_exporter = JaegerExporter(
    # NOTE: we use environment variables to use Jaeger collector
    # collector_endpoint='http://jaeger-collector.istio-system:14268/api/traces?format=jaeger.thrift'
    # agent_host_name="localhost",
    # agent_port=6831
)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "sample-istio"})
    )
)
# Get the base tracer
tracer = trace.get_tracer(__name__)
# Create a batch processor with Jaeger expoerter and set it
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()

# Decorator
def traceit(name):
    def wrapper(f):
        @wraps(f)
        async def inner(*args, **kwargs):
            request = kwargs.get('request')
            ctx = B3MultiFormat().extract(dict(request.headers))
            with tracer.start_as_current_span(name, context=ctx):
                return await f(*args, **kwargs)
        return inner
    return wrapper

@app.get("/")
@traceit("main")
async def root(request: Request):
    # Get current span
    span = trace.get_current_span()
    span.set_attribute("level", 0)
    # Get User from DB
    await _get_user_info_from_db()
    # Create a Meme with AI
    await _create_ai_meme()
    return {"message": "hi, someone is tracing me!"}


async def _get_user_info_from_db():

    # Simulates get user data from DB
    with tracer.start_as_current_span('user-from-db') as span:
        time.sleep(random.random())
        span.set_attribute('level', 1)
        span.set_attribute('user_id', '1234')

async def _create_ai_meme():

    # Simulates a AI/ML call
    with tracer.start_as_current_span('ml-image') as span:
        time.sleep(random.random())
        span.set_attribute('level', 1)
        with tracer.start_as_current_span('ml-image:download-random-image') as nested_span:
            time.sleep(random.random())
            # Here it's interesting to pass propagate the traces
            # headers = {}
            # B3MultiFormat().inject(headers)
            # requests.get(..., headers=headers)
            nested_span.set_attribute('level', 2)
            nested_span.set_attribute('service.http.status', 200)
            nested_span.set_attribute('image.id', 'img-{}'.format(random.randint(100, 10000)))
        with tracer.start_as_current_span('ml-image:run-inference') as nested_span:
            time.sleep(random.random())
            nested_span.set_attribute('level', 2)
            nested_span.set_attribute('memory.used', '2921MB')
        span.set_attribute('ml.confidence', '{}%'.format(random.randint(0, 100)))
