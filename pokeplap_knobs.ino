// PokePlap Hardware Interface Core
// Maps physical linear or rotary faders to the simulation engine

const int CORTISOL_PIN = A0;  // Connect your physical dial's center pin to Analog Pin 0
int lastPotValue = 0;
const int noiseThreshold = 3; // Built-in filter to eliminate signal jitter

void setup() {
  // Open hardware serial communication line over USB
  Serial.begin(9600);
}

void loop() {
  // Read raw electrical voltage from the dial (0 to 1023)
  int currentPotValue = analogRead(CORTISOL_PIN);
  
  // Only transmit data if a human actively turned the dial past the noise threshold
  if (abs(currentPotValue - lastPotValue) > noiseThreshold) {
    
    // Map the raw electrical signal into your biological platform scale (0.0 to 30.0 µg/dL)
    float simulatedCortisol = (currentPotValue / 1023.0) * 30.0;
    
    // Print structured stream data to the Serial buffer
    // Expected daemon format -> "cortisol:VALUE"
    Serial.print("cortisol:");
    Serial.println(simulatedCortisol, 1); // 1 decimal point precision
    
    // Update structural tracking baseline
    lastPotValue = currentPotValue;
  }
  
  delay(50); // 50ms interval loop to protect serial interface bandwidth
}
