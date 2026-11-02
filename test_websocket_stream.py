import asyncio
import json
import random
import websockets

# Your live production Fly.io WebSocket URL
LIVE_WS_URL = "ws://pokeplap.fly.dev/api/v1/stream"

async def simulate_live_pokes():
    print(f"Connecting to live PokePlap production server at: {LIVE_WS_URL}...")
    
    try:
        async with websockets.connect(LIVE_WS_URL) as websocket:
            print("✅ Connection established successfully!")
            print("Starting automated virtual telemetry simulation injection...\n")
            
            # Simulate a clinician clicking and dragging a timeline slider 5 times
            for i in range(1, 6):
                # Generate a simulated fluctuating cortisol value (e.g., between 5.0 and 25.0 µg/dL)
                simulated_value = round(random.uniform(5.0, 25.0), 1)
                
                # Build the structured variable poke payload frame
                payload = {
                    "event": "variable_poke",
                    "source": "virtual_testing_daemon",
                    "variable": "cortisol",
                    "value": simulated_value,
                    "timeline_index": i
                }
                
                print(f"[TX] Sending Poke Event #{i}: Aligned cortisol to {simulated_value} µg/dL...")
                await websocket.send(json.dumps(payload))
                
                # Instantly catch the broadcasted recalculation sent back by the server
                response = await websocket.recv()
                server_data = json.loads(response)
                
                print(f"[RX] Server Broadcast Received!")
                print(f"     Source Node: {server_data.get('source')}")
                print(f"     Computed Vitals State Matrix: {server_data.get('simulated_metrics')}\n")
                
                # Wait 2 seconds between injection intervals
                await asyncio.sleep(2)
                
            print("🏆 Virtual testing loop completed successfully. All frames processed without errors.")
            
    except Exception as e:
        print(f"❌ Connection or runtime stream failure: {e}")

if __name__ == "__main__":
    # Execute the asynchronous test loop
    asyncio.run(simulate_live_pokes())
