import asyncio
import json
import random
import websockets

# Your live secured production Fly.io WebSocket URL with authentication token parameter
LIVE_WS_URL = "ws://pokeplap.fly.dev/api/v1/stream?token=poke_secure_2026"

async def simulate_live_pokes():
    print(f"Connecting to live PokePlap production server at: {LIVE_WS_URL}...")
    
    try:
        async with websockets.connect(LIVE_WS_URL) as websocket:
            print("✅ Secured connection established successfully!")
            print("Starting automated virtual telemetry simulation injection...\n")
            
            for i in range(1, 6):
                simulated_value = round(random.uniform(5.0, 25.0), 1)
                
                payload = {
                    "event": "variable_poke",
                    "source": "virtual_testing_daemon",
                    "variable": "cortisol",
                    "value": simulated_value,
                    "timeline_index": i
                }
                
                print(f"[TX] Sending Secure Poke Event #{i}: Cortisol to {simulated_value} µg/dL...")
                await websocket.send(json.dumps(payload))
                
                response = await websocket.recv()
                server_data = json.loads(response)
                
                print(f"[RX] Authenticated Server Broadcast Received!")
                print(f"     Source Node: {server_data.get('source')}")
                print(f"     Stored Ledger State: {server_data.get('simulated_metrics')}\n")
                
                await asyncio.sleep(2)
                
            print("🏆 Secured testing loop completed successfully.")
            
    except Exception as e:
        print(f"❌ Connection or authentication stream failure: {e}")

if __name__ == "__main__":
    asyncio.run(simulate_live_pokes())
