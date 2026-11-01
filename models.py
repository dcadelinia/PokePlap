from pydantic import BaseModel
from typing import Dict, List, Optional 

class PhysiologicalState(BaseModel):
"""
Represents a complete snapshot of a biological organism's vital
metrics at a discrete point in simulated time.
"""
timestamp_seq: int  # Sequential step tracker (0, 1, 2...)
heart_rate: float   # bpm
blood_pressure_systolic: float # mmHg
oxygen_saturation: float       # % (0.0 to 1.0)
endocrine_cortisol: float      # mcg/dL (Sample metabolic marker) 

class TimelineState(BaseModel):
"""
Represents the active control plane state of the simulation timeline.
"""
current_step: int
max_history_steps: int
is_paused: bool
