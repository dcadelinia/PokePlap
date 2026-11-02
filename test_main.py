import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from main import app

client = TestClient(app)

def test_root_status():
    """Verify base verification router behaves normally."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["platform"] == "PokePlap"

def test_health_check_endpoint():
    """Verify automated health check endpoint responds successfully."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "active_ws_streams" in response.json()
    assert response.json()["status"] == "healthy"

def test_websocket_security_rejection():
    """Verify connections without a valid security token are dropped with policy violation."""
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/stream?token=invalid_key") as websocket:
            pass
    # WS 1008 indicates policy violation / bad authorization token
    assert excinfo.value.code == 1008

def test_websocket_secured_handshake():
    """Verify connections with the exact matching security credential establish a connection."""
    with client.websocket_connect("/api/v1/stream?token=poke_secure_2026") as websocket:
        # Send a baseline ping to verify active pipeline
        payload = {
            "event": "variable_poke",
            "source": "automated_unit_test",
            "variable": "cortisol",
            "value": 15.5,
            "timeline_index": 1
        }
        websocket.send_json(payload)
        response = websocket.receive_json()
        assert response["status"] == "computed"
        assert response["target_variable"] == "cortisol"
        assert response["new_value"] ==15.5
