from prometheus_client import (
    Counter,
    Histogram
)

INCIDENT_COUNTER = Counter(
    "incident_requests_total",
    "Total incidents"
)

PROCESSING_TIME = Histogram(
    "incident_processing_seconds",
    "Incident processing duration"
)
TRIAGE_COUNTER = Counter(
    "triage_agent_executions_total",
    "Total triage agent executions"
)

RAG_COUNTER = Counter(
    "knowledge_agent_executions_total",
    "Total knowledge agent executions"
)

REMEDIATION_COUNTER = Counter(
    "remediation_agent_executions_total",
    "Total remediation agent executions"
)

NOTIFIER_COUNTER = Counter(
    "notifier_agent_executions_total",
    "Total notifier agent executions"
)