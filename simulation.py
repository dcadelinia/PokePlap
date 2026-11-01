from typing import Dict, Optional
from models import PhysiologicalState, TimelineState
from kinematics_engine import BiologicalKinematicsEngine 

class BiologicalDigitalTwinTimeline:
"""
Manages the persistent timeline state array for the ICU digital twin.
Implements a strict historical state ledger for non-deterministic rewinding
and accelerated forward-projection loops for fast-forwarding.
"""
def **init**(self, initial_state: PhysiologicalState, max_history: int = 1000):
self.max_history = max_history
self.current_step = initial_state.timestamp_seq 

### Historical snapshot cache (Key: step_id -> Value: PhysiologicalState)

# Crucial for rewinding complex biological vectors that cannot run in reverse

self.history_ledger: Dict[int, PhysiologicalState] = {
self.current_step: initial_state
}

def get_current_state(self) -> PhysiologicalState:
"""Retrieves the physiological state at the current timeline head."""
return self.history_ledger[self.current_step] 

def process_realtime_step(self, dt: float = 1.0) -> PhysiologicalState:
"""Advances the digital twin normally by one step using the physics engine."""
current = self.get_current_state()
next_state = BiologicalKinematicsEngine.project_next_state(current, dt) 

### Track history & update timeline pointer

self.current_step = next_state.timestamp_seq
self.history_ledger[self.current_step] = next_state 

# Evict old history frames if cache limits are reached

if len(self.history_ledger) > self.max_history:
oldest_key = min(self.history_ledger.keys())
del self.history_ledger[oldest_key]

return next_state

def poke_variable(self, variable_name: str, value: float) -> PhysiologicalState:
"""
Allows clinicians to dynamically intervene ('poke') a biometric parameter
at the current frame, mutating the trajectory of all future updates.
"""
current = self.get_current_state()
state_dict = current.model_dump() 

if variable_name in state_dict:
state_dict[variable_name] = value
# Re-instantiate mutated frame over current timeline position
mutated_state = PhysiologicalState(**state_dict)
self.history_ledger[self.current_step] = mutated_state
return mutated_state
else:
raise ValueError(f"Variable '{variable_name}' does not exist in biological profile.")
def rewind(self, steps_back: int) -> PhysiologicalState:
"""
Rewinds the biological digital twin by pulling historical states
from the explicit snapshot register.
"""
target_step = max(min(self.history_ledger.keys()), self.current_step - steps_back)
self.current_step = target_step
return self.get_current_state() 

def fast_forward(self, total_minutes: float, processing_dt: float = 1.0) -> PhysiologicalState:
"""
Fast-forwards the simulation into the future by breaking the jumped
interval into precise differential blocks and executing an accelerated projection loop.
"""
steps_to_run = int(total_minutes / processing_dt) 

for _ in range(steps_to_run):
current = self.get_current_state()
### Generate next step dynamically using the mathematical projection matrices

next_state = BiologicalKinematicsEngine.project_next_state(current, processing_dt) 

    # Map into our timeline ledger
    self.current_step = next_state.timestamp_seq
    self.history_ledger[self.current_step] = next_state
    
return self.get_current_state()

if **name** == "**main**":
print("Initializing PokePlap Timeline Engine...") 

patient_zero = PhysiologicalState(
timestamp_seq=0,
heart_rate=95.0,
blood_pressure_systolic=135.0,
oxygen_saturation=0.9800,
endocrine_cortisol=24.5
)

twin_timeline = BiologicalDigitalTwinTimeline(initial_state=patient_zero)
print(f"Step 0 Baseline: {twin_timeline.get_current_state()}")

for _ in range(5):
twin_timeline.process_realtime_step(dt=1.0)
print(f"Step 5 (Normal Decay): {twin_timeline.get_current_state()}")

print("\n[CLINICIAN INTERVENTION] - Poking Cortisol levels to spike up to 50.0mcg/dL...")
twin_timeline.poke_variable("endocrine_cortisol", 50.0)

print("Projecting timeline forward 15 minutes dynamically...")
twin_timeline.fast_forward(total_minutes=15.0, processing_dt=1.0)
print(f"Step 20 (Predictive Future State): {twin_timeline.get_current_state()}")

print("\n[CLINICIAN TIMELINE REWIND] - Scrubbing back 10 steps into cached memory registry...")
twin_timeline.rewind(steps_back=10)
print(f"Step 10 (Restored Snapshot State): {twin_timeline.get_current_state()}")
