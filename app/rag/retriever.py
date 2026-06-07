from app.rag.vector_store import db


def retrieve_context(query):
    """
    Retrieve relevant context from the vector database.

    Responsibilities:
    1. Perform semantic similarity search.
    2. Retrieve the most relevant documents.
    3. Combine retrieved content into a single context string.
    """

    # Search the vector database for documents
    # most similar to the input query.
    # k=2 returns the top 2 matching documents.
    docs = db.similarity_search(
        query,
        k=2
    )

    # Combine retrieved document contents
    # into a single context string for the LLM.
    return "\n".join(
        [d.page_content for d in docs]
    )