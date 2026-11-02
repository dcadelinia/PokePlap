import pytest
from fastapi.testclient import TestClient
from payment_routes import router
from fastapi import FastAPI

# Spin up a sandboxed application context to trace financial routers independent of main
test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)

def test_checkout_session_rejection_on_invalid_tier():
    """Confirms server drops bad parameters with bad request errors before reaching stripe channels."""
    response = client.post("/api/v1/billing/checkout/session?tier=non_existent_tier")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid target subscription tier."

def test_webhook_signature_rejection():
    """Confirms the webhook handler drops traffic containing invalid headers to avoid spoofing loops."""
    mock_payload = {
        "id": "evt_test_123",
        "type": "checkout.session.completed",
        "data": {"object": {"customer": "cus_123", "subscription": "sub_123"}}
    }
    # Passing an invalid or missing stripe signature must force a 400 validation rejection
    response = client.post(
        "/api/v1/billing/webhook", 
        json=mock_payload,
        headers={"stripe-signature": "invalid_signature_metadata_hash"}
    )
    assert response.status_code == 400
