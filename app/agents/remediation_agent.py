from app.llm import llm
from app.logger import log_event
from app.metrics import REMEDIATION_COUNTER

from app.tools.cleanup_disk import cleanup_disk
from app.tools.restart_service import restart_service
from app.tools.rollback_deployment import rollback_deployment


def remediation_agent(state):
    """
    Remediation Agent.

    Responsibilities:
    1. Generate remediation recommendations.
    2. Use incident details and retrieved context.
    3. Invoke approved remediation tools when safe.
    4. Support human approval for risky actions.
    5. Track execution metrics and logs.
    """

    # Log agent start event
    log_event(
        "remediation_agent",
        "started",
        state.get("trace_id"),
        {
        "category": state["category"]
        }
    )

    # Increment remediation agent execution count
    REMEDIATION_COUNTER.inc()

    # Build prompt using incident details and retrieved context
    prompt = f"""
    Incident:
    {state['incident']}

    Context:
    {state['context']}

    Provide remediation steps.
    """

    # Generate remediation recommendations
    result = llm.invoke(prompt)

    tool_name = "None"
    tool_result = "No tool executed"

    category = state.get(
        "category",
        ""
    ).lower()

    entities = state.get(
        "entities",
        []
    )

    # Use first extracted entity if available
    target = (
        entities[0]
        if entities
        else "unknown"
    )
    if category == "deployment":
        tool_name = "rollback_deployment"
        tool_result = rollback_deployment.invoke(
            {
                "version": target
            }
        )
    # Safe automated actions
    elif state["severity"] in [
        "P2",
        "P3",
        "P4"
    ]:

        if (
            "disk" in category
            or "storage" in category
            or "infra" in category
        ):
            tool_name = "cleanup_disk"
            tool_result = cleanup_disk.invoke(
                {
                    "server": target
                }
            )

        elif (
            "service" in category
            or "application" in category
        ):
            tool_name = "restart_service"  
            tool_result = restart_service.invoke(
                {
                    "service_name": target
                }
            )

        elif "deployment" in category:
            tool_name = "rollback_deployment"
            tool_result = rollback_deployment.invoke(
                {
                    "version": target
                }
            )

    # Log completion
    log_event(
        "remediation_agent",
        "completed",
        state.get("trace_id"),
        {
        "tool_result": tool_result
        }
    )

    return {
        "remediation": result.content,
        "tool_name": tool_name,
        "tool_result": tool_result
    }
    
