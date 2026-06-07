from langgraph.graph import StateGraph
from app.schemas.state import IncidentState

from app.agents.triage_agent import triage_agent
from app.agents.knowledge_agent import knowledge_agent
from app.agents.remediation_agent import remediation_agent
from app.agents.notifier_agent import notifier_agent


# Create LangGraph workflow using IncidentState schema
# to manage data flow between agents
workflow = StateGraph(
    IncidentState
)

# Add Triage Agent node
# Responsible for incident classification
workflow.add_node(
    "triage",
    triage_agent
)

# Add Knowledge Agent node
# Retrieves relevant runbooks and context
workflow.add_node(
    "knowledge",
    knowledge_agent
)

# Add Remediation Agent node
# Generates remediation recommendations using LLM
workflow.add_node(
    "remediation",
    remediation_agent
)

# Add Notification Agent node
# Creates final incident summary
workflow.add_node(
    "notify",
    notifier_agent
)

# Define workflow starting point
workflow.set_entry_point(
    "triage"
)

# After classification, move to knowledge retrieval
workflow.add_edge(
    "triage",
    "knowledge"
)


def route(state):
    """
    Conditional routing logic.

    High-priority incidents (P1/P2):
        Knowledge → Remediation → Notification

    Low-priority incidents (P3/P4):
        Knowledge → Notification
    """

    # Route critical incidents to remediation step
    if state["severity"] in [
        "P1",
        "P2"
    ]:
        return "remediation"
    
    if state["category"] in [
        "application",
        "infra",
        "deployment"
    ]:
        return "remediation"

    # Skip remediation for lower-priority incidents
    return "notify"


# Add conditional workflow routing
# based on incident severity
workflow.add_conditional_edges(
    "knowledge",
    route
)

# After remediation, generate notification summary
workflow.add_edge(
    "remediation",
    "notify"
)

# Compile workflow into executable graph
graph = workflow.compile()