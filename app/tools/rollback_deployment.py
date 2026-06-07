from langchain.tools import tool


@tool
def rollback_deployment(version: str):
    """
    Roll back deployment to the specified version.
    """

    return {
        "status": "rolled_back",
        "version": version
    }