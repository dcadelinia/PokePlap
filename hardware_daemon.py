import asyncio
import json
import serial
import websockets

# Configuration settings matching your micro-controller interface setup
SERIAL_PORT = '/dev/ttyACM0'  # Use 'COM3' or similar if testing on Windows
BAUD_RATE = 9600
BACKEND_WS_URL = 'ws://localhost:8000/api/v1/stream'

async def read_hardware_dials():
    print(f"Opening physical serial connection on {SERIAL_PORT}...")
    try:
        # Establish connection with the physical control surface
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    except Exception as e:
        print(f"Hardware Error: Could not connect to serial port {SERIAL_PORT}. {e}")
        return

    print(f"Connecting to PokePlap WebSocket infrastructure at {BACKEND_WS_URL}...")
    async with websockets.connect(BACKEND_WS_URL) as websocket:
        print("Connected. Turn physical dials to send real-time variables.")
        
        while True:
            if ser.in_waiting > 0:
                try:
                    # Read the line printed out by your hardware micro-controller
                    raw_line = ser.readline().decode('utf-8').strip()
                    
                    # Expecting format: "cortisol:12.5" or "heart_rate:85"
                    if ":" in raw_line:
                        var_name, var_val = raw_line.split(":")
                        
                        # Build the asynchronous payload frame
                        hardware_payload = {
                            "event": "variable_poke",
                            "source": "hardware_fader_chassis",
                            "variable": var_name.strip(),
                            "value": float(var_val.strip()),
                            "timeline_index": 0
                        }
                        
                        # Push the change up to the core simulation immediately
                        await websocket.send(json.dumps(hardware_payload))
                        print(f"Hardware Sync: Moved {var_name} -> {var_val}")
                        
                except Exception as error:
                    print(f"Frame processing error: {error}")
                    
            await asyncio.sleep(0.01) # 10ms poll rate to protect compute cycles

if __name__ == "__main__":
    try:
        asyncio.run(read_hardware_dials())
    except KeyboardInterrupt:
        print("\nHardware daemon shut down cleanly.")
import serial.tools.list_ports

def find_active_usb_channels():
    print("Scanning system for physical hardware controllers...")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ No active USB Serial hardware detected. Check your cable connection.")
        return
        
    for port in ports:
        print(f" Detected Port: {port.device}")
        print(f"   Description: {port.description}")
        print(f"   Hardware ID: {port.hwid}\n")
        print(f"👉 Use '{port.device}' inside your hardware_daemon.py script configuration.")

if __name__ == "__main__":
    find_active_usb_channels
    ()
