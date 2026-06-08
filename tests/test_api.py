import pytest
import requests
import os

BASE_URL = os.environ.get("BASE_URL", "http://3.106.156.32:32500")

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data

def test_predict_returns_label_and_confidence():
    payload = {"text": "This is a great product"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["confidence"] <= 1
    assert "model_version" in data

def test_predict_negative_text():
    payload = {"text": "This is terrible and awful"}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200

def test_health_returns_model_version_unstable():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "unstable-v1"