from typing import TypedDict


class IncidentState(TypedDict):
    """Shared workflow state passed between LangGraph agents."""
    trace_id: str
    incident: str
    severity: str
    category: str
    entities: list
    context: str
    remediation: list[str]
    tool_name: str
    tool_result: dict
    summary: str
