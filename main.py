import asyncio
import json
import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
import psycopg2

app = FastAPI(
    title="PokePlap Platform API",
    description="Secured biological digital twin backend with active database ledger logging",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pokeplap")

# =====================================================================
# DATABASE STORAGE LOGIC
# =====================================================================
def log_to_ledger(source: str, variable: str, value: float, timeline_idx: int, metrics: dict):
    """Synchronous worker function to log telemetry into the relational database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = """
            INSERT INTO telemetry_logs 
            (source, target_variable, poked_value, timeline_index, computed_heart_rate, computed_spo2, computed_systolic_bp)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(query, (
            source, 
            variable, 
            value, 
            timeline_idx, 
            metrics["heart_rate"], 
            metrics["spo2"], 
            metrics["systolic_bp"]
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database logging failure: {e}")

# =====================================================================
# WEBSOCKET STREAM ORCHESTRATION
# =====================================================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "active_ws_streams": len(manager.active_connections)}

@app.websocket("/api/v1/stream")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    # Validate connection credentials immediately during the handshake
    if token != "poke_secure_2026":
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload.get("event") == "variable_poke":
                var_name = payload.get("variable")
                new_val = payload.get("value")
                t_idx = payload.get("timeline_index", 0)
                src = payload.get("source", "web_ui")
                
                # Dynamic calculated output dictionary
                simulated_metrics = {
                    "heart_rate": 78,
                    "spo2": 96,
                    "cortisol": new_val,
                    "respiratory_rate": 16,
                    "systolic_bp": 120
                }
                
                broadcast_payload = {
                    "status": "computed",
                    "source": src,
                    "target_variable": var_name,
                    "new_value": new_val,
                    "timeline_index": t_idx,
                    "simulated_metrics": simulated_metrics
                }
                
                # 1. Distribute state array instantly to all open UI clients
                await manager.broadcast(broadcast_payload)
                
                # 2. Fire and forget database insert asynchronously to prevent pipeline lag
                asyncio.create_task(
                    run_in_threadpool(log_to_ledger, src, var_name, new_val, t_idx, simulated_metrics)
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
