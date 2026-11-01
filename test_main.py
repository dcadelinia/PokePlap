import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app) 

def test_health_and_infrastructure_heartbeat():
response = client.get("/health")
assert response.status_code == 200
assert response.json()["status"] == "healthy" 

def test_unauthorized_license_key_rejection():
payload = {
"sector_id": "aquaculture",
"license_key": "BAD-MALICIOUS-TOKEN-123"
}
response = client.post("/initialize-sector", json=payload)
assert response.status_code == 401
assert "Invalid or expired Enterprise License Token" in response.json()["detail"] 

def test_subscription_tier_feature_gate():
payload = {
"sector_id": "bio_logistics",
"license_key": "SKU-CLINICAL-FREE-99"
}
response = client.post("/initialize-sector", json=payload)
assert response.status_code == 403
assert "Access Denied" in response.json()["detail"] 

def test_aquaculture_physics_informed_matrix():
init_payload = {
"sector_id": "aquaculture",
"license_key": "SKU-AQUA-PRO-77X"
}
init_res = client.post("/initialize-sector", json=init_payload)
assert init_res.status_code == 200 

step_res = client.post("/step")
assert step_res.status_code == 200
metrics_after_step = step_res.json()["state"]["metrics"]
assert "dissolved_oxygen" in metrics_after_step

poke_payload = {"variable_name": "nitrogen_level", "value": 5.5}
poke_res = client.post("/poke", json=poke_payload)
assert poke_res.status_code == 200

ff_payload = {"minutes": 10.0}
ff_res = client.post("/fast-forward", json=ff_payload)
assert ff_res.status_code == 200

final_metrics = ff_res.json()["state"]["metrics"]
assert final_metrics["dissolved_oxygen"] < 95.0

def test_bio_logistics_cold_chain_spoilage():
init_payload = {
"sector_id": "bio_logistics",
"license_key": "SKU-GLOBAL-ENTERPRISE-DYNAMIC-MATRIX"
}
init_res = client.post("/initialize-sector", json=init_payload)
assert init_res.status_code == 200 

client.post("/poke", json={"variable_name": "ambient_temp", "value": 15.0})

ff_res = client.post("/fast-forward", json={"minutes": 30.0})
final_metrics = ff_res.json()["state"]["metrics"]
assert final_metrics["payload_decay_index"] > 0.0

def test_historical_timeline_rewind_buffer():
client.post("/initialize-sector", json={
"sector_id": "icu_human",
"license_key": "SKU-CLINICAL-FREE-99"
}) 

client.post("/step")
client.post("/step")
step_three = client.post("/step").json()
step_three_seq = step_three["current_step"]

rw_res = client.post("/rewind", json={"steps": 2})
assert rw_res.status_code == 200
assert rw_res.json()["current_step"] == step_three_seq - 2

if **name** == "**main**":
import sys
sys.exit(pytest.main(["-v", **file**]))
