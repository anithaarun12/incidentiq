from app.rag.retriever import retrieve_context
from app.logger import log_event
from app.metrics import RAG_COUNTER


def knowledge_agent(state):
    """
    Knowledge Retrieval Agent.

    Responsibilities:
    1. Retrieve relevant runbook/context information.
    2. Track agent execution metrics.
    3. Log execution status for monitoring and debugging.
    """

    # Log agent start event
    log_event(
        "knowledge_agent",
        "started",
        state.get("trace_id"),
        {
        "incident": state["incident"]
        }
    )

    # Increment knowledge retrieval agent execution count
    RAG_COUNTER.inc()

    # Retrieve relevant context based on incident description
    context = retrieve_context(
        state["incident"]
    )

    # Log successful completion of context retrieval
    log_event(
        "knowledge_agent",
        "completed",
        state.get("trace_id"),
        {
        "context_length": len(context)
        }
    )

    # Return retrieved context to the workflow
    return {
        "context": context
    }