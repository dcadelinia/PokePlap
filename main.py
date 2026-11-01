# ==========================================
# FILE: main.py
# ==========================================
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any

# Core engine imports
from models import PhysiologicalState
from simulation import BiologicalDigitalTwinTimeline

app = FastAPI(
    title="PokePlap Core API",
    description="Enterprise-grade Biological Digital Twin Temporal Orchestration Engine",
    version="1.0.0"
)

# Enable seamless multi-port or cross-origin browser communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory instantiation of the Patient Digital Twin 
# Initialized with a stressed clinical ICU baseline profile
initial_patient = PhysiologicalState(
    timestamp_seq=0,
    heart_rate=92.0,
    blood_pressure_systolic=130.0,
    oxygen_saturation=0.9850,
    endocrine_cortisol=20.0
)
timeline = BiologicalDigitalTwinTimeline(initial_state=initial_patient)

@app.get("/health", tags=["Infrastructure"])
async def health_check():
    """System heartbeat checkpoint verifying pipeline integrity."""
    return {"status": "healthy", "engine": "NVIDIA-AI-Accelerated-Twin"}

@app.get("/telemetry", tags=["Simulation Engine"])
async def get_current_telemetry():
    """Fetches the state matrix active at the current timeline playhead cursor."""
    return {
        "current_step": timeline.current_step,
        "state": timeline.get_current_state()
    }

@app.post("/step", tags=["Simulation Engine"])
async def advance_timeline_step(dt: float = 1.0):
    """Calculates and appends a single forward homeostatic increment frame."""
    next_state = timeline.process_realtime_step(dt=dt)
    return {"message": "Timeline stepped forward", "state": next_state, "current_step": timeline.current_step}

@app.post("/poke", tags=["Clinical Interventions"])
async def poke_biometric_variable(
    variable_name: str = Body(..., embed=True), 
    value: float = Body(..., embed=True)
):
    """Mutates an independent biological variable at the current frame marker."""
    try:
        updated_state = timeline.poke_variable(variable_name, value)
        return {
            "message": f"Successfully poked variable: {variable_name}",
            "state": updated_state,
            "current_step": timeline.current_step
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rewind", tags=["Temporal Controls"])
async def scrub_timeline_backwards(steps: int = Body(..., embed=True)):
    """Restores the digital twin back to a past state snapshot ledger entry."""
    restored_state = timeline.rewind(steps_back=steps)
    return {
        "message": f"Timeline wound back {steps} frames",
        "state": restored_state,
        "current_step": timeline.current_step
    }

@app.post("/fast-forward", tags=["Temporal Controls"])
async def project_timeline_forward(minutes: float = Body(..., embed=True)):
    """Accelerates background calculations to project patient metrics forward into the future."""
    projected_state = timeline.fast_forward(total_minutes=minutes)
    return {
        "message": f"Timeline accelerated forward by {minutes} simulation minutes",
        "state": projected_state,
        "current_step": timeline.current_step
    }

# Entrypoint for optional manual standalone script launches
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
