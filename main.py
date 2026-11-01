# ==========================================
# FILE: main.py
# ==========================================
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from models import SystemStateMatrix, SectorConfig
from simulation import UniversalDigitalTwinTimeline
from typing import Dict, Any

app = FastAPI(title="PokePlap Enterprise Matrix API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active Global Deployment Matrix Registries
SECTOR_REGISTRY = {
    "icu_human": SectorConfig(
        sector_id="icu_human",
        base_targets={"heart_rate": 70.0},
        decay_rates={"cortisol_clearance": 0.05},
        interaction_coefficients={}
    ),
    "aquaculture": SectorConfig(
        sector_id="aquaculture",
        base_targets={"dissolved_oxygen": 95.0, "nitrogen_level": 0.5, "water_temp": 22.0, "native_plant_efficiency": 85.0},
        decay_rates={"nitrogen_clearance": 0.03},
        interaction_coefficients={}
    ),
    "bio_logistics": SectorConfig(
        sector_id="bio_logistics",
        base_targets={"ambient_temp": 4.0},
        decay_rates={"thermal_leak": 0.04},
        interaction_coefficients={"spoilage_multiplier": 1.8}
    ),
    "datacenter_symbiosis": SectorConfig(
        sector_id="datacenter_symbiosis",
        base_targets={"coolant_heat_output": 35.0},
        decay_rates={"heat_transfer": 0.15},
        interaction_coefficients={}
    )
}

INITIAL_STATES = {
    "icu_human": {"heart_rate": 90.0, "blood_pressure_systolic": 130.0, "endocrine_cortisol": 25.0},
    "aquaculture": {"dissolved_oxygen": 95.0, "nitrogen_level": 0.8, "water_temp": 23.0, "native_plant_efficiency": 80.0},
    "bio_logistics": {"ambient_temp": 4.5, "payload_decay_index": 0.0},
    "datacenter_symbiosis": {"computing_load_pct": 45.0, "coolant_heat_output": 38.0, "soil_moisture": 65.0, "greenhouse_humidity": 75.0}
}

# Default Active Boot Parameter Base Configuration Target
current_sector = "icu_human"
timeline = UniversalDigitalTwinTimeline(
    initial_state=SystemStateMatrix(timestamp_seq=0, metrics=INITIAL_STATES[current_sector]),
    config=SECTOR_REGISTRY[current_sector]
)

@app.post("/initialize-sector")
async def initialize_sector(sector_id: str = Body(..., embed=True)):
    global timeline, current_sector
    if sector_id not in SECTOR_REGISTRY:
        raise HTTPException(status_code=400, detail="Invalid target platform expansion sector profile identifier.")
    
    current_sector = sector_id
    timeline = UniversalDigitalTwinTimeline(
        initial_state=SystemStateMatrix(timestamp_seq=0, metrics=INITIAL_STATES[sector_id].copy()),
        config=SECTOR_REGISTRY[sector_id]
    )
    return {"message": f"Engine initialized successfully for sector: {sector_id}", "current_step": timeline.current_step}

@app.get("/telemetry")
async def get_telemetry():
    return {"current_step": timeline.current_step, "sector": current_sector, "metrics": timeline.get_current_state().metrics}

@app.post("/step")
async def process_step():
    return {"state": timeline.process_realtime_step(), "current_step": timeline.current_step}

@app.post("/poke")
async def execute_poke(variable_name: str = Body(..., embed=True), value: float = Body(..., embed=True)):
    try:
        updated = timeline.poke_variable(variable_name, value)
        return {"state": updated, "current_step": timeline.current_step}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rewind")
async def rewind_timeline(steps: int = Body(..., embed=True)):
    return {"state": timeline.rewind(steps), "current_step": timeline.current_step}

@app.post("/fast-forward")
async def fast_forward_timeline(minutes: float = Body(..., embed=True)):
    return {"state": timeline.fast_forward(minutes), "current_step": timeline.current_step}
