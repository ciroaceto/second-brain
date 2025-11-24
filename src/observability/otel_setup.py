import logging
import time
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from src.evaluation.metrics import collector

# Setup logging - only show warnings and errors by default
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Silence verbose third-party loggers
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("opentelemetry").setLevel(logging.ERROR)
logging.getLogger("mem0").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)

# Setup tracing with service name
resource = Resource.create({"service.name": "second-brain"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Add console exporter (for local debugging) - disabled by default
# Set OTEL_CONSOLE_TRACES=true to enable console output
if os.getenv("OTEL_CONSOLE_TRACES", "false").lower() == "true":
    console_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace.get_tracer_provider().add_span_processor(console_processor)

# Add OTLP exporter for Jaeger (if enabled)
# Set OTEL_EXPORTER_OTLP_ENDPOINT environment variable or default to localhost
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
try:
    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        insecure=True  # For local development
    )
    otlp_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(otlp_processor)
    # logger.info(f"OpenTelemetry traces will be exported to {otlp_endpoint}")
except Exception as e:
    # Silently continue if Jaeger is not available
    pass

def trace_function(func):
    """Decorator to trace function calls."""
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                collector.record(f"{func.__name__}.latency", time.time() - start)
                collector.record(f"{func.__name__}.success", 1)
                return result
            except Exception as e:
                collector.record(f"{func.__name__}.error", 1)
                logger.error(f"Error in {func.__name__}: {e}")
                raise
    return wrapper

