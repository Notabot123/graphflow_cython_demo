# tests/test_backend_api.py
import sys, os
import pytest
from fastapi.testclient import TestClient

# Ensure backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def startup():
    """Ensure app startup events run (load modules)."""
    with TestClient(app) as c:
        yield c

def test_nodes_endpoint():
    """Check that /api/nodes returns at least one node."""
    response = client.get("/api/nodes")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert any("Image Filter" in n["name"] for n in data["nodes"])

def test_ui_endpoint():
    """Check that /ui returns HTML with node list."""
    response = client.get("/ui")
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Registered Nodes" in response.text
