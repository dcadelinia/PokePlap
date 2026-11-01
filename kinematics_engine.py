import math
from models import PhysiologicalState 

class BiologicalKinematicsEngine:
"""
Physics-informed modeling engine that projects biological state mutations
forward over discrete time deltas (dt) based on active physiological variables.
""" 

@staticmethod
def project_next_state(current: PhysiologicalState, dt: float) -> PhysiologicalState:
"""
Applies simplified biophysical differential equations to project the next
physiological state array after an elapsed time delta (dt in minutes).
"""
### --- Biological Decay and Homeostatic Constants ---

CORTISOL_DECAY_RATE = 0.05  # Metabolic clearance rate per minute
BASE_HEART_RATE = 70.0      # Homeostatic target
HEART_RATE_RECOVERY = 0.1   # Rate of return to baseline per minute 

### 1. Endocrine Decay (Exponential clearance)

### d[Cortisol]/dt = -k * [Cortisol]

new_cortisol = current.endocrine_cortisol * math.exp(-CORTISOL_DECAY_RATE * dt)
if new_cortisol < 2.0:  # Floor baseline
new_cortisol = 2.0 

### 2. Heart Rate Response to Endocrine / Homeostatic Pull

### High cortisol drives elevated heart rate; system naturally decays back to baseline

hr_drive = (current.endocrine_cortisol - 5.0) * 1.5
target_hr = BASE_HEART_RATE + max(0.0, hr_drive) 

### Simple Euler integration step for Heart Rate adjustment

hr_delta = (target_hr - current.heart_rate) * HEART_RATE_RECOVERY * dt
new_hr = current.heart_rate + hr_delta 

### 3. Blood Pressure Coupling

### Systolic linked directly to vascular resistance and cardiac output proxies

target_bp = 120.0 + (new_hr - BASE_HEART_RATE) * 0.4
bp_delta = (target_bp - current.blood_pressure_systolic) * 0.2 * dt
new_bp = current.blood_pressure_systolic + bp_delta 

### 4. Oxygen Saturation Homeostasis

### Decreases slightly under severe tachycardic strain for simulation dynamics

if new_hr > 130:
spo2_decay = 0.005 * (new_hr - 130) * dt
new_spo2 = max(0.70, current.oxygen_saturation - spo2_decay)
else:
new_spo2 = min(1.0, current.oxygen_saturation + (1.0 - current.oxygen_saturation) * 0.1 * dt) 

return PhysiologicalState(
timestamp_seq=current.timestamp_seq + 1,
heart_rate=round(new_hr, 2),
blood_pressure_systolic=round(new_bp, 2),
oxygen_saturation=round(new_spo2, 4),
endocrine_cortisol=round(new_cortisol, 3)
)
