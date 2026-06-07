# IncidentIQ - Agentic AI Incident Management System

## Overview

IncidentIQ is an Agentic AI-powered incident management platform that automates incident triage, knowledge retrieval, remediation recommendation, and notification generation.

The system uses a multi-agent architecture built with FastAPI, LangGraph, LangChain, ChromaDB, and Prometheus.

Key capabilities:

* Multi-agent orchestration using LangGraph
* Retrieval-Augmented Generation (RAG)
* Structured outputs using Pydantic
* Automated remediation tool invocation
* Prometheus metrics and observability
* Trace ID-based request tracking
* Docker and Kubernetes deployment support

---

# Architecture Diagram

```text
                +----------------+
                |    FastAPI     |
                |  /process API  |
                +--------+-------+
                         |
                         v
                +----------------+
                | LangGraph Flow |
                +--------+-------+
                         |
                         v
                +----------------+
                | Triage Agent   |
                | Structured LLM |
                +--------+-------+
                         |
                         v
                +----------------+
                | Knowledge Agent|
                |  RAG Retrieval |
                +--------+-------+
                         |
                Conditional Route
                         |
         +---------------+--------------+
         |                              |
         v                              v
 +----------------+            +----------------+
 | Remediation    |            | Notifier Agent |
 | Agent          |            +----------------+
 +-------+--------+
         |
         v
 +-------------------------+
 | Mock Tools              |
 | cleanup_disk()          |
 | restart_service()       |
 | rollback_deployment()   |
 +-------------------------+
         |
         v
 +----------------+
 | Final Response |
 +----------------+

RAG Components:
Incidents + Runbooks
        ↓
Document Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Similarity Search
```

---

# Agent Architecture

## 1. Triage Agent

Responsibilities:

* Classifies incident severity
* Identifies incident category
* Extracts relevant entities
* Uses structured output with Pydantic

Example Output:

```json
{
  "severity": "P2",
  "category": "infra",
  "entities": ["server01"]
}
```

---

## 2. Knowledge Agent

Responsibilities:

* Retrieves historical incidents
* Retrieves operational runbooks
* Uses ChromaDB vector search
* Provides context for remediation

---

## 3. Remediation Agent

Responsibilities:

* Generates remediation recommendations
* Invokes operational tools when safe
* Produces corrective actions

Supported Tools:

| Tool                | Purpose             |
| ------------------- | ------------------- |
| cleanup_disk        | Storage cleanup     |
| restart_service     | Service recovery    |
| rollback_deployment | Deployment rollback |

---

## 4. Notifier Agent

Responsibilities:

* Generates final summary
* Creates response payload
* Consolidates remediation results

---

# LangGraph Workflow

```text
User Incident
      ↓
Triage Agent
      ↓
Knowledge Agent
      ↓
Conditional Routing
      ↓
Remediation Agent
      ↓
Notifier Agent
      ↓
Final Response
```

---

# Conditional Routing

The workflow uses LangGraph conditional routing.

Routing Logic:

* deployment incidents → Remediation Agent
* application incidents → Remediation Agent
* infrastructure incidents → Remediation Agent
* unknown incidents → Notifier Agent

This demonstrates dynamic agent orchestration.

---

# RAG Pipeline

Knowledge Sources:

### Historical Incidents

Location:

```text
data/incidents.json
```

### Runbooks

Location:

```text
data/runbooks/
```

Examples:

* database_pool_exhausted.md
* disk_full.md
* dns_failure.md
* deployment_rollback.md
* oomkilled.md

RAG Flow:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Similarity Search
    ↓
Retrieved Context
```

Embedding Model:

```text
all-MiniLM-L6-v2
```

Vector Store:

```text
ChromaDB
```

---

# Technology Stack

* Python 3.11
* FastAPI
* LangGraph
* LangChain
* ChromaDB
* Sentence Transformers
* Pydantic
* Prometheus
* Docker
* Kubernetes

---

# Project Structure

```text
incidentiq/

├── app/
│   ├── agents/
│   ├── graph/
│   ├── rag/
│   ├── schemas/
│   ├── tools/
│   ├── metrics.py
│   ├── logger.py
│   └── main.py
│
├── data/
│   ├── incidents.json
│   └── runbooks/
│
├── tests/
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Process Incident

```http
POST /process
```

Request:

```json
{
  "incident": "Disk usage exceeded 95% on server01"
}
```

---

## Incident Lookup

```http
GET /incident/{id}
```

Example:

```http
GET /incident/INC-001
```

---

## Prometheus Metrics

```http
GET /metrics
```

---

## Custom Metrics

```http
GET /custom-metrics
```

Example:

```text
incident_requests_total 5
triage_agent_executions_total 5
knowledge_agent_executions_total 5
remediation_agent_executions_total 5
notifier_agent_executions_total 5
```

---

# Observability

## Trace ID

Each request is assigned a unique Trace ID.

Example:

```json
{
  "trace_id": "6f32e14c-15d4-4e7f-a495-5d36b11b09d6"
}
```

The Trace ID is propagated across:

* Triage Agent
* Knowledge Agent
* Remediation Agent
* Notifier Agent

and included in structured JSON logs.

---

## Metrics

Available Metrics:

* incident_requests_total
* incident_processing_seconds
* triage_agent_executions_total
* knowledge_agent_executions_total
* remediation_agent_executions_total
* notifier_agent_executions_total

---

# Evaluation Metrics

The following metrics were used to evaluate system performance:

## Response Latency

Measured using:

```text
incident_processing_seconds
```

Observed Average:

```text
~28 ms using MockLLM
```

## API Success Rate

Measures successful HTTP responses.

## Agent Execution Metrics

Tracks execution counts for each agent.

---

# Running the Application

## Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Build Knowledge Base

```bash
python app/rag/ingest.py
```

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Metrics:

```text
http://127.0.0.1:8000/metrics
```

---

# Docker Support

Build:

```bash
docker build -t incidentiq .
```

Run:

```bash
docker run -p 8000:8000 incidentiq
```

Note:

Docker validation was not performed in the current development environment because Docker was not installed locally. The Dockerfile has been included as part of the project deliverables.

---

# Kubernetes Deployment

Apply manifests:

```bash
kubectl apply -f k8s/
```

---

# CI/CD

GitHub Actions workflow included:

```text
.github/workflows/ci.yml
```

Pipeline Steps:

* Install dependencies
* Run tests
* Validate Docker build

---

# Testing

Run tests:

```bash
pytest tests/test_process.py -v
```

Result:

```text
4 passed
```

Covered APIs:

* POST /process
* GET /health
* GET /incident/{id}
* GET /custom-metrics

---

# Demo Walkthrough

## Scenario 1 - Disk Space Incident

```bash
curl -X POST http://localhost:8000/process \
-H "Content-Type: application/json" \
-d '{"incident":"Disk usage exceeded 95% on server01"}'
```

Expected:

* Infra classification
* RAG retrieval
* cleanup_disk() invocation
* Summary generation

---

## Scenario 2 - Service Outage

```bash
curl -X POST http://localhost:8000/process \
-H "Content-Type: application/json" \
-d '{"incident":"Customer portal service customer-portal is unavailable"}'
```

Expected:

* Application classification
* restart_service() invocation
* Final notification

---

## Scenario 3 - Failed Deployment

```bash
curl -X POST http://localhost:8000/process \
-H "Content-Type: application/json" \
-d '{"incident":"Deployment version v2.1.5 introduced production failures"}'
```

Expected:

* Deployment classification
* rollback_deployment() invocation
* Final summary generation

```
```
