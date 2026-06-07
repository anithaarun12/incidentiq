from langchain.tools import tool


@tool
def cleanup_disk(server: str):
    """
    Perform disk cleanup on the specified server.
    """

    return {
        "status": "cleaned",
        "server": server
    }