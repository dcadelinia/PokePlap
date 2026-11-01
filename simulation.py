from typing import Dict
from models import SystemStateMatrix, SectorConfig
from kinematics_engine import UniversalKinematicsEngine 

class UniversalDigitalTwinTimeline:
"""
Manages state ledger indexing architectures across disparate sectors.
Bakes in history array serialization for non-linear chronological travel.
"""
def **init**(self, initial_state: SystemStateMatrix, config: SectorConfig, max_history: int = 2000):
self.config = config
self.max_history = max_history
self.current_step = initial_state.timestamp_seq
self.history_ledger: Dict[int, SystemStateMatrix] = {self.current_step: initial_state} 

def get_current_state(self) -> SystemStateMatrix:
return self.history_ledger[self.current_step]

def process_realtime_step(self, dt: float = 1.0) -> SystemStateMatrix:
current = self.get_current_state()
next_state = UniversalKinematicsEngine.calculate_next_frame(current, self.config, dt)
self.current_step = next_state.timestamp_seq
self.history_ledger[self.current_step] = next_state

if len(self.history_ledger) > self.max_history:
    del self.history_ledger[min(self.history_ledger.keys())]
    
return next_state

def poke_variable(self, variable_name: str, value: float) -> SystemStateMatrix:
current = self.get_current_state()
if variable_name not in current.metrics:
raise ValueError(f"Variable '{variable_name}' is invalid in the {self.config.sector_id} profile.")
current.metrics[variable_name] = value
self.history_ledger[self.current_step] = current
return current

def rewind(self, steps_back: int) -> SystemStateMatrix:
target_step = max(min(self.history_ledger.keys()), self.current_step - steps_back)
self.current_step = target_step
return self.get_current_state()

def fast_forward(self, total_minutes: float, processing_dt: float = 1.0) -> SystemStateMatrix:
steps = int(total_minutes / processing_dt)
for _ in range(steps):
current = self.get_current_state()
next_state = UniversalKinematicsEngine.calculate_next_frame(current, self.config, processing_dt)
self.current_step = next_state.timestamp_seq
self.history_ledger[self.current_step] = next_state
return self.get_current_state()
