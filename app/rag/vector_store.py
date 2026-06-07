from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import (
    SentenceTransformerEmbeddings
)

# Initialize embedding model used to convert
# text into vector representations for
# semantic similarity search.
embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Load the persisted Chroma vector database.
# The same embedding model must be used during
# both ingestion and retrieval to ensure
# consistent vector representations.
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)