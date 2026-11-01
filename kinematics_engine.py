# ==========================================
# FILE: kinematics_engine.py
# ==========================================
import math
from models import SystemStateMatrix, SectorConfig

class UniversalKinematicsEngine:
    """
    Universal mathematical projection engine that processes cross-variable 
    decay mechanics and homeostatic balances across distinct sectors.
    """
    
    @staticmethod
    def calculate_next_frame(current: SystemStateMatrix, config: SectorConfig, dt: float) -> SystemStateMatrix:
        """
        Applies parameterized differential equations tailored dynamically 
        to the executing deployment configuration profile over delta time (dt).
        """
        new_metrics = current.metrics.copy()
        s_id = config.sector_id

        # ----------------------------------------------------------------
        # SECTOR EXPANSION 1: Aquaculture Closed-Loop Biome Track
        # ----------------------------------------------------------------
        if s_id == "aquaculture":
            # Variables: dissolved_oxygen (%), nitrogen_level (ppm), water_temp (C), native_plant_efficiency (%)
            # Nitrogen decays naturally via plant filtration, but drops if plant efficiency falls
            plant_eff = new_metrics.get("native_plant_efficiency", 80.0)
            nitro_decay = (config.decay_rates.get("nitrogen_clearance", 0.04) * (plant_eff / 100.0))
            
            new_metrics["nitrogen_level"] = max(0.1, new_metrics.get("nitrogen_level", 1.2) * math.exp(-nitro_decay * dt))
            
            # Water temperature shifts drive accelerated nitrogen accumulation if too high
            temp = new_metrics.get("water_temp", 22.0)
            if temp > 26.0:
                new_metrics["nitrogen_level"] += 0.08 * (temp - 26.0) * dt
            
            # High nitrogen stresses organisms, driving down dissolved oxygen proxy thresholds
            if new_metrics["nitrogen_level"] > 3.0:
                oxygen_drop = 0.05 * (new_metrics["nitrogen_level"] - 3.0) * dt
                new_metrics["dissolved_oxygen"] = max(30.0, new_metrics.get("dissolved_oxygen", 95.0) - oxygen_drop)
            else:
                new_metrics["dissolved_oxygen"] = min(100.0, new_metrics.get("dissolved_oxygen", 95.0) + 0.2 * dt)

        # ----------------------------------------------------------------
        # SECTOR EXPANSION 2: Bio-Logistics Fragile Cold Chain Track
        # ----------------------------------------------------------------
        elif s_id == "bio_logistics":
            # Variables: ambient_temp (C), container_humidity (%), transit_delay_mins (min), payload_decay_index (0-100)
            # Internal cold loop decay rate vs external atmospheric penetration
            ext_temp = new_metrics.get("ambient_temp", 4.0)
            base_target_temp = config.base_targets.get("ambient_temp", 4.0)
            
            # Thermal insulation leak formula
            temp_leak = (ext_temp - base_target_temp) * config.decay_rates.get("thermal_leak", 0.02) * dt
            current_temp = new_metrics.get("ambient_temp", 4.0) + temp_leak
            new_metrics["ambient_temp"] = round(current_temp, 2)
            
            # Payload degradation curve triggers if refrigeration boundary line breaks
            if current_temp > 8.0:
                damage_factor = (current_temp - 8.0) * config.interaction_coefficients.get("spoilage_multiplier", 1.5) * dt
                new_metrics["payload_decay_index"] = min(100.0, new_metrics.get("payload_decay_index", 0.0) + damage_factor)
            else:
                new_metrics["payload_decay_index"] = max(0.0, new_metrics.get("payload_decay_index", 0.0) - 0.05 * dt)

        # ----------------------------------------------------------------
        # SECTOR EXPANSION 3: Data Center Thermodynamic Greenhouses
        # ----------------------------------------------------------------
        elif s_id == "datacenter_symbiosis":
            # Variables: computing_load_pct (%), coolant_heat_output (C), soil_moisture (%), greenhouse_humidity (%)
            load = new_metrics.get("computing_load_pct", 50.0)
            target_heat = 30.0 + (load * 0.5) # Direct scale multiplier
            
            heat_delta = (target_heat - new_metrics.get("coolant_heat_output", 40.0)) * config.decay_rates.get("heat_transfer", 0.1) * dt
            new_metrics["coolant_heat_output"] = round(new_metrics.get("coolant_heat_output", 40.0) + heat_delta, 2)
            
            # Extreme hot plumes accelerate dehydration profiles in connected botanical microclimates
            current_heat = new_metrics["coolant_heat_output"]
            if current_heat > 55.0:
                evap_rate = (current_heat - 55.0) * 0.12 * dt
                new_metrics["soil_moisture"] = max(10.0, new_metrics.get("soil_moisture", 60.0) - evap_rate)
                new_metrics["greenhouse_humidity"] = max(20.0, new_metrics.get("greenhouse_humidity", 70.0) - evap_rate * 0.5)

        # ----------------------------------------------------------------
        # BASE LAYER: Core Legacy Clinical ICU Framework Track
        # ----------------------------------------------------------------
        else:
            cortisol_decay = config.decay_rates.get("cortisol_clearance", 0.05)
            new_cortisol = new_metrics.get("endocrine_cortisol", 20.0) * math.exp(-cortisol_decay * dt)
            new_metrics["endocrine_cortisol"] = max(2.0, new_cortisol)
            
            hr_drive = (new_metrics["endocrine_cortisol"] - 5.0) * 1.5
            target_hr = config.base_targets.get("heart_rate", 70.0) + max(0.0, hr_drive)
            new_hr = new_metrics.get("heart_rate", 80.0) + (target_hr - new_metrics.get("heart_rate", 80.0)) * 0.1 * dt
            new_metrics["heart_rate"] = new_hr

            target_bp = 120.0 + (new_hr - 70.0) * 0.4
            new_metrics["blood_pressure_systolic"] = new_metrics.get("blood_pressure_systolic", 120.0) + (target_bp - new_metrics.get("blood_pressure_systolic", 120.0)) * 0.2 * dt

        # Global round optimization iteration map pass
        for k in new_metrics:
            new_metrics[k] = round(new_metrics[k], 4)

        return SystemStateMatrix(
            timestamp_seq=current.timestamp_seq + 1,
            metrics=new_metrics,
            metadata=current.metadata
 )
