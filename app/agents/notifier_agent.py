from app.logger import log_event
from app.metrics import NOTIFIER_COUNTER


def notifier_agent(state):
    """
    Notification Agent.

    Responsibilities:
    1. Generate a human-readable incident summary.
    2. Include severity, category, and remediation details.
    3. Track agent execution metrics.
    4. Log execution status for monitoring and auditing.
    """

    # Log agent start event
    log_event(
        "notifier_agent",
        "started",
        state.get("trace_id")
    )

    # Increment notifier agent execution count
    NOTIFIER_COUNTER.inc()

    remediation = state.get(
        "remediation",
        "No remediation generated"
    )

    tool_name = state.get(
        "tool_name",
        "No tool selected"
    )
    tool_result = state.get(
        "tool_result",
        "No tool executed"
    )
    # Create formatted incident summary for notification/reporting
    summary = f"""
    Severity: {state['severity']}

    Category: {state['category']}

    Recommendation:

    {remediation}

    Tool Executed:

    {tool_name}

    Tool Result:
    
    {tool_result}

    """

    # Log successful completion of notification generation
    log_event(
        "notifier_agent",
        "completed",
        state.get("trace_id"),
        {
        "severity": state["severity"]
        }
    )

    # Return generated summary to the workflow
    return {
        "summary": summary
    }