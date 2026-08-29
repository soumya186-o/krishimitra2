import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.seed_data import seed_database

# Ensure database is created and seeded for testing
seed_database()

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "KrishiMitra Backend"

def test_get_crops():
    response = client.get("/api/v1/crops")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    crop_names = [c["name_en"] for c in data]
    assert any("Rice" in name for name in crop_names)
    assert any("Wheat" in name for name in crop_names)

def test_get_crop_by_id():
    response = client.get("/api/v1/crops/rice")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "rice"
    assert "Clayey" in data["soil"]

def test_get_schemes():
    response = client.get("/api/v1/schemes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    scheme_ids = [s["id"] for s in data]
    assert "pm_kisan" in scheme_ids
    assert "pmfby" in scheme_ids

def test_get_loans():
    response = client.get("/api/v1/loans")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_weather():
    response = client.get("/api/v1/weather?district=delhi")
    assert response.status_code == 200
    data = response.json()
    assert "current_temperature" in data
    assert "agri_advisory" in data
    assert len(data["forecast"]) >= 3

def test_ai_query_hindi():
    payload = {
        "query": "धान के लिए कौन सी मिट्टी अच्छी है?",
        "language": "hi"
    }
    response = client.post("/api/v1/ai/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_intent"] == "soil"
    assert data["is_verified_fact"] is True
    assert "मिट्टी" in data["answer"] or "दोमट" in data["answer"]

def test_ai_query_english():
    payload = {
        "query": "What fertilizer does wheat need?",
        "language": "en"
    }
    response = client.post("/api/v1/ai/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["detected_intent"] == "fertilizer"
    assert "NPK" in data["answer"]

def test_sync():
    response = client.get("/api/v1/sync")
    assert response.status_code == 200
    data = response.json()
    assert data["crops_count"] >= 10
    assert data["schemes_count"] >= 5
    assert data["diseases_count"] >= 10
