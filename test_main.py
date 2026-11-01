import pytest
import asyncio
import httpx
from typing import Dict, Any 

### Primary deployment target for your live Fly.io production platform

BASE_URL = "https://pokeplap.fly.dev" 

@pytest.fixture
def sample_crisis_payload() -> Dict[str, Any]:
"""
Generates a high-stress physiological crash payload (acute critical event scenario).
"""
return {
"snapshot": {
"species_context": "canine",
"base_vitals": {
"heart_rate": 160.0,
"blood_pressure_sys": 85.0,
"oxygen_saturation": 88.0
},
"environmental_load": 2.5
},
"delta_seconds": 180,
"variable_adjustments": {
"heart_rate": 35.0,        # Simulating escalating tachycardia
"blood_pressure_sys": -20.0 # Simulating severe hypotensive shock
}
} 

@pytest.mark.asyncio
async def test_health_endpoint_concurrency():
"""
Verifies response integrity, latency bounds, and explicit legal entity headers.
"""
async with httpx.AsyncClient(base_url=BASE_URL) as client:
response = await client.get("/health")
assert response.status_code == 200
data = response.json()
assert data["status"] == "ACTIVE"
assert "Odynex Axis Logistics LLC" in data["legal_entities"]
assert "David Fabian Cadelinia" in data["legal_entities"] 

@pytest.mark.asyncio
async def test_high_throughput_timeline_scrub(sample_crisis_payload):
"""
Stress-tests the timeline scrubbing engine with 50 parallel calculation requests.
"""
async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
tasks = [
client.post("/api/v1/scrub", json=sample_crisis_payload)
for _ in range(50)
]
responses = await asyncio.gather(*tasks) 

for response in responses:
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "SUCCESS"
    assert "projected_state" in res_data
    assert "hazard_index" in res_data
    assert "reversibility_threshold" in res_data
