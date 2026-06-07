from langchain.tools import tool


@tool
def restart_service(service_name: str):
    """
    Restart the specified application service.
    """

    return {
        "status": "success",
        "service": service_name
    }