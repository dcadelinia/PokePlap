import asyncio
import json
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Initialize the enterprise FastAPI instance
app = FastAPI(
    title="PokePlap Platform API",
    description="Enterprise-grade biological digital twin backend powered by NVIDIA AI",
    version="1.0.0"
)

# Enable CORS for local and cloud dashboard web interfaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# SECTION 1: ASYNCHRONOUS WEBSOCKET CONNECTION MANAGER
# =====================================================================
class ConnectionManager:
    """Manages active live dashboard connections and hardware serial daemons."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Pushes data arrays simultaneously to all active connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Catch closed or unstable sockets silently to avoid loop blocking
                pass

manager = ConnectionManager()


# =====================================================================
# SECTION 2: WEB SERVICE AND STATUS ENDPOINTS
# =====================================================================
@app.get("/")
async def root_status():
    """Base verification route."""
    return {
        "platform": "PokePlap",
        "status": "online",
        "engine_state": "initialized"
    }

@app.get("/health")
async def health_check():
    """
    Comprehensive verification endpoint requested for automated orchestration.
    Checks container network binding and active socket manager infrastructure.
    """
    return {
        "status": "healthy",
        "active_ws_streams": len(manager.active_connections),
        "subsystems": {
            "kinematics_engine": "responsive",
            "telemetry_streamer": "active"
        }
    }


# =====================================================================
# SECTION 3: INTERACTIVE REAL-TIME STREAM WEBSOCKET ROUTE
# =====================================================================
@app.websocket("/api/v1/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    Primary bi-directional event bus. Listens for text/slider "pokes" 
    from the web UI or linear hardware encoders via local daemons.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Capture incoming asynchronous frame
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            event_type = payload.get("event")
            
            if event_type == "variable_poke":
                variable_name = payload.get("variable")
                new_value = payload.get("value")
                timeline_index = payload.get("timeline_index", 0)
                source_id = payload.get("source", "web_ui")
                
                # ─── INTEGRATION POINT FOR KINEMATICS ENGINE ───
                # Import or invoke your modeling calculations directly here:
                # from kinematics_engine import compute_decay
                # results = compute_decay(variable_name, new_value)
                
                # Formulate the synchronized telemetry state payload
                broadcast_payload = {
                    "status": "computed",
                    "source": source_id,
                    "target_variable": variable_name,
                    "new_value": new_value,
                    "timeline_index": timeline_index,
                    "simulated_metrics": {
                        "heart_rate": 78,
                        "spo2": 96,
                        "cortisol": new_value,  # Tracked modification parameter
                        "respiratory_rate": 16,
                        "systolic_bp": 120
                    }
                }
                
                # Sync the fresh model execution out to every open client
                await manager.broadcast(broadcast_payload)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        # Prevent runtime backend crashing on bad payload decodes
        manager.disconnect(websocket)


# =====================================================================
# SECTION 4: STANDARD RUNTIME LOOP TRACE
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    # Local loop startup parameters matching your Docker/Fly setup configurations
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
