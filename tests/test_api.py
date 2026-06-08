import pytest
import requests

# Base URL of the running app
BASE_URL = "http://3.106.156.32:32500"

def test_health_endpoint():
    """Test GET /health returns 200 with status healthy and model_version present."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data

def test_predict_returns_label_and_confidence():
    """Test POST /predict returns label, confidence, and model_version."""
    payload = {"text": "This is a great product"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["confidence"] <= 1
    assert "model_version" in data

def test_predict_negative_text():
    """Test POST /predict with negative text returns 200."""
    payload = {"text": "This is terrible and awful"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200

def test_health_returns_model_version_unstable():
    """Test GET /health returns exactly unstable-v1 as model_version."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "unstable-v1"