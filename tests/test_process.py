from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_process_incident():

    payload = {
        "incident": "Database Pool Exhausted"
    }

    response = client.post(
        "/process",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "severity" in data
    assert "category" in data
    assert "context" in data
    assert "remediation" in data
    assert "summary" in data


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_incident_lookup():

    response = client.get(
        "/incident/INC-001"
    )

    assert response.status_code == 200

def test_custom_metrics():

    response = client.get(
        "/custom-metrics"
    )

    assert response.status_code == 200

    assert "incident_requests_total" in response.text
