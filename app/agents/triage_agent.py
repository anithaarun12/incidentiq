from app.llm import llm
from app.schemas.models import IncidentClassification
from app.logger import log_event
from app.metrics import TRIAGE_COUNTER


# Configure LLM to return structured output
# matching the IncidentClassification schema
structured_llm = llm.with_structured_output(
    IncidentClassification
)


def triage_agent(state):
    """
    Triage Agent.

    Responsibilities:
    1. Analyze incoming incident descriptions.
    2. Classify severity (P1-P4).
    3. Identify incident category.
    4. Extract relevant entities.
    5. Track execution metrics and logs.
    """

    # Log agent start event
    log_event(
        "triage_agent",
        "started",
        state.get("trace_id"),
        {
        "incident": state["incident"]
        }
    )

    # Increment triage agent execution count
    TRIAGE_COUNTER.inc()

    # Create classification prompt for the LLM
    prompt = f"""
Classify the incident.

Incident:
{state['incident']}

Return:

1. severity (P1-P4)
2. category
3. entities

Valid categories:
- infra
- application
- deployment
- database
- network

Examples:

Incident:
Disk usage exceeded 95% on server01
Category: infra
Entities: ["server01"]

Incident:
Customer portal service customer-portal is unavailable
Category: application
Entities: ["customer-portal"]

Incident:
Deployment version v2.1.5 introduced production failures
Category: deployment
Entities: ["v2.1.5"]

Return only structured output.
"""

    # Invoke structured LLM to classify the incident
    result = structured_llm.invoke(state["incident"])

    # Log successful completion of classification
    log_event(
        "triage_agent",
        "completed",
        state.get("trace_id"),
        {
        "severity": result.severity,
        "category": result.category
        }
    )

    # Return structured classification results
    return {
        "severity": result.severity,
        "category": result.category,
        "entities": result.entities
    }