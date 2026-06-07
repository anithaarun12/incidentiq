from fastapi import FastAPI
from fastapi import Response
import json
from app.logger import get_trace_id
from fastapi.responses import StreamingResponse
# Import Prometheus metrics counters and histogram
from app.metrics import (
    INCIDENT_COUNTER,
    TRIAGE_COUNTER,
    RAG_COUNTER,
    REMEDIATION_COUNTER,
    NOTIFIER_COUNTER,
    PROCESSING_TIME
)

# LangGraph workflow for incident processing
from app.graph.workflow import graph

# Request schema for incident input validation
from app.schemas.models import IncidentRequest

# Prometheus metrics exporter
from prometheus_client import generate_latest

# Initialize FastAPI application
app = FastAPI()

@app.get("/stream")
async def stream():

    async def event_generator():

        yield "data: Triage completed\n\n"

        yield "data: Knowledge completed\n\n"

        yield "data: Remediation completed\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.get("/health")
def health():
    """
    Health check endpoint.
    Used by monitoring tools and load balancers
    to verify that the application is running.
    """
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():
    """
    Exposes Prometheus metrics.
    Prometheus scrapes this endpoint to collect
    application performance and usage metrics.
    """
    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.post("/process")
def process_incident(request: IncidentRequest):
    """
    Main incident processing endpoint.

    Steps:
    1. Increment incident request counter.
    2. Measure end-to-end processing time.
    3. Invoke LangGraph workflow.
    4. Return generated response.
    """

    # Increment total incident requests count
    INCIDENT_COUNTER.inc()

    # Measure request processing time
    with PROCESSING_TIME.time():

        trace_id = get_trace_id()

        # Execute multi-agent workflow
        result = graph.invoke(
            {
                "incident": request.incident,
                "trace_id": trace_id
            }
        )

    return {
    "trace_id": trace_id,
    "result": result
}


@app.get("/incident/{incident_id}")
def get_incident(incident_id: str):
    """
    Retrieve incident details from JSON datastore
    using incident ID.
    """

    # Load incident records
    with open("data/incidents.json") as f:
        incidents = json.load(f)

    # Search for matching incident
    for incident in incidents:
        if incident["id"] == incident_id:
            return incident

    # Return message if incident not found
    return {
        "message": "Incident not found"
    }


@app.get("/custom-metrics")
def custom_metrics():
    """
    Custom metrics endpoint displaying
    individual agent execution counts.
    Useful for debugging and reporting.
    """

    metrics = f"""
incident_requests_total {INCIDENT_COUNTER._value.get()}

triage_agent_executions_total {TRIAGE_COUNTER._value.get()}

knowledge_agent_executions_total {RAG_COUNTER._value.get()}

remediation_agent_executions_total {REMEDIATION_COUNTER._value.get()}

notifier_agent_executions_total {NOTIFIER_COUNTER._value.get()}
"""

    return Response(
        metrics,
        media_type="text/plain"
    )