import json
import os
from pathlib import Path

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import (
    SentenceTransformerEmbeddings
)

# ---------------------------------------
# Load Incident Records
# ---------------------------------------
# Read historical incident data from JSON
# and convert each record into a LangChain
# Document for vector indexing.

docs = []

with open("data/incidents.json", "r") as f:
    incidents = json.load(f)

for item in incidents:

    docs.append(
        Document(
            page_content=f"""
Title: {item['title']}

Description:
{item['description']}

Severity:
{item.get('severity', 'Unknown')}

Category:
{item.get('category', 'Unknown')}

Resolution:
{item['resolution']}
            """,
            metadata={
                "source": "incident",
                "id": item["id"]
            }
        )
    )

print(f"Loaded {len(incidents)} incidents")

# ---------------------------------------
# Load Runbook Documents
# ---------------------------------------
# Read operational runbooks from the
# runbooks directory and add them to
# the document collection.

runbook_path = Path("data/runbooks")

for file in runbook_path.glob("*.md"):

    with open(file, "r", encoding="utf-8") as f:

        content = f.read()

        docs.append(
            Document(
                page_content=content,
                metadata={
                    "source": "runbook",
                    "file_name": file.name
                }
            )
        )

print(
    f"Loaded {len(list(runbook_path.glob('*.md')))} runbooks"
)

# ---------------------------------------
# Chunk Documents
# ---------------------------------------
# Split large documents into smaller chunks
# to improve retrieval accuracy and relevance.

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunked_docs = text_splitter.split_documents(docs)

print(
    f"Created {len(chunked_docs)} document chunks"
)

# ---------------------------------------
# Create Embedding Model
# ---------------------------------------
# Convert text documents into vector
# representations using a lightweight
# Sentence Transformer model.

embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ---------------------------------------
# Build Chroma Vector Database
# ---------------------------------------
# Generate embeddings for all documents
# and store them in a persistent ChromaDB
# vector database for semantic search.

db = Chroma.from_documents(
    documents=chunked_docs,
    embedding=embedding,
    persist_directory="./chroma_db"
)

# Persist vector database to disk
# so it can be reused without re-indexing.
db.persist()

print(
    f"Ingestion complete. Total chunks indexed: {len(chunked_docs)}"
)