import logging
import uuid
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def log_event(
        agent,
        event,
        trace_id=None,
        data=None
):
    """
    Log structured JSON events with a shared trace ID.
    """

    payload = {
        "trace_id": trace_id,
        "agent": agent,
        "event": event,
        "data": data
    }

    logger.info(
        json.dumps(payload)
    )


def get_trace_id():
    """
    Generate a unique trace ID for each request.
    """
    return str(uuid.uuid4())