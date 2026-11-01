# ==========================================
# FILE: main.py - PART 1 OF 4
# ==========================================
import os
import math
import stripe
from fastapi import FastAPI, HTTPException, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List

# Initialize Core Enterprise Application Framework
app = FastAPI(
    title="PokePlap Enterprise Matrix Core",
    description="Unified Digital Twin Chronological Projection & Monetization Engine",
    version="2.1.0"
)

# Enable seamless multi-port or cross-origin browser communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Production Billing Credentials securely from active container environments
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_placeholder_key_if_empty")

# ==========================================
# DATA OBJECT ARCHITECTURES
# ==========================================
class SystemStateMatrix(BaseModel):
    timestamp_seq: int = Field(..., description="Sequential simulation frame index")
    metrics: Dict[str, float] = Field(..., description="Dynamic key-value array for variable parameters")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Context definitions")

class SectorConfig(BaseModel):
    sector_id: str
    base_targets: Dict[str, float]
    decay_rates: Dict[str, float]
    interaction_coefficients: Dict[str, float]

class SubscriptionTier(BaseModel):
    tier_name: str
    allowed_sectors: List[str]
    max_history_buffer: int
    allow_custom_pokes: bool
    rate_limit_ff_mins:float
    # ==========================================
# FILE: main.py - PART 2 OF 4
# ==========================================

# ==========================================
# ENTERPRISE MONETIZATION MAPS
# ==========================================
SUBSCRIPTION_PLANS: Dict[str, SubscriptionTier] = {
    "plan_icu_basic": SubscriptionTier(
        tier_name="Clinical Free Trial",
        allowed_sectors=["icu_human"],
        max_history_buffer=100,
        allow_custom_pokes=True,
        rate_limit_ff_mins=30.0
    ),
    "plan_agtech_pro": SubscriptionTier(
        tier_name="AgTech Professional License",
        allowed_sectors=["icu_human", "aquaculture"],
        max_history_buffer=1000,
        allow_custom_pokes=True,
        rate_limit_ff_mins=120.0
    ),
    "plan_global_matrix": SubscriptionTier(
        tier_name="Global Matrix Unlimited Enterprise",
        allowed_sectors=["icu_human", "aquaculture", "bio_logistics", "datacenter_symbiosis"],
        max_history_buffer=5000,
        allow_custom_pokes=True,
        rate_limit_ff_mins=1440.0
    )
}

VALID_LICENSE_KEYS: Dict[str, str] = {
    "SKU-CLINICAL-FREE-99": "plan_icu_basic",
    "SKU-AQUA-PRO-77X": "plan_agtech_pro",
    "SKU-GLOBAL-ENTERPRISE-DYNAMIC-MATRIX": "plan_global_matrix"
}

PLAN_PRICE_IDS = {
    "plan_icu_basic": os.getenv("STRIPE_PRICE_ICU", "price_mock_icu_basic"),
    "plan_agtech_pro": os.getenv("STRIPE_PRICE_AGTECH", "price_mock_agtech_pro"),
    "plan_global_matrix": os.getenv("STRIPE_PRICE_GLOBAL", "price_mock_global_matrix")
}

TIER_TOKENS = {
    "plan_icu_basic": "SKU-CLINICAL-FREE-99",
    "plan_agtech_pro": "SKU-AQUA-PRO-77X",
    "plan_global_matrix": "SKU-GLOBAL-ENTERPRISE-DYNAMIC-MATRIX"
}

# ==========================================
# SECTOR REGISTRY AND INITIAL STATE MATRICES
# ==========================================
SECTOR_REGISTRY = {
    "icu_human": SectorConfig(sector_id="icu_human", base_targets={"heart_rate": 70.0}, decay_rates={"cortisol_clearance": 0.05}, interaction_coefficients={}),
    "aquaculture": SectorConfig(sector_id="aquaculture", base_targets={"dissolved_oxygen": 95.0, "nitrogen_level": 0.5, "water_temp": 22.0, "native_plant_efficiency": 85.0}, decay_rates={"nitrogen_clearance": 0.03}, interaction_coefficients={}),
    "bio_logistics": SectorConfig(sector_id="bio_logistics", base_targets={"ambient_temp": 4.0}, decay_rates={"thermal_leak": 0.04}, interaction_coefficients={"spoilage_multiplier": 1.8}),
    "datacenter_symbiosis": SectorConfig(sector_id="datacenter_symbiosis", base_targets={"coolant_heat_output": 35.0}, decay_rates={"heat_transfer": 0.15}, interaction_coefficients={})
}

INITIAL_STATES = {
    "icu_human": {"heart_rate": 90.0, "blood_pressure_systolic": 130.0, "endocrine_cortisol": 25.0},
    "aquaculture": {"dissolved_oxygen": 95.0, "nitrogen_level": 0.8, "water_temp": 23.0, "native_plant_efficiency": 80.0},
    "bio_logistics": {"ambient_temp": 4.5, "payload_decay_index": 0.0},
    "datacenter_symbiosis": {"computing_load_pct": 45.0, "coolant_heat_output": 38.0, "soil_moisture": 65.0, "greenhouse_humidity": 75.0}
}
# ==========================================
# FILE: main.py - PART 3 OF 4
# ==========================================

# ==========================================
# KINEMATICS EQUATIONS
# ==========================================
class UniversalKinematicsEngine:
    @staticmethod
    def calculate_next_frame(current: SystemStateMatrix, config: SectorConfig, dt: float) -> SystemStateMatrix:
        new_metrics = current.metrics.copy()
        s_id = config.sector_id

        if s_id == "aquaculture":
            plant_eff = new_metrics.get("native_plant_efficiency", 80.0)
            nitro_decay = (config.decay_rates.get("nitrogen_clearance", 0.04) * (plant_eff / 100.0))
            new_metrics["nitrogen_level"] = max(0.1, new_metrics.get("nitrogen_level", 1.2) * math.exp(-nitro_decay * dt))
            temp = new_metrics.get("water_temp", 22.0)
            if temp > 26.0:
                new_metrics["nitrogen_level"] += 0.08 * (temp - 26.0) * dt
            if new_metrics["nitrogen_level"] > 3.0:
                oxygen_drop = 0.05 * (new_metrics["nitrogen_level"] - 3.0) * dt
                new_metrics["dissolved_oxygen"] = max(30.0, new_metrics.get("dissolved_oxygen", 95.0) - oxygen_drop)
            else:
                new_metrics["dissolved_oxygen"] = min(100.0, new_metrics.get("dissolved_oxygen", 95.0) + 0.2 * dt)

        elif s_id == "bio_logistics":
            ext_temp = new_metrics.get("ambient_temp", 4.0)
            base_target_temp = config.base_targets.get("ambient_temp", 4.0)
            temp_leak = (ext_temp - base_target_temp) * config.decay_rates.get("thermal_leak", 0.02) * dt
            current_temp = new_metrics.get("ambient_temp", 4.0) + temp_leak
            new_metrics["ambient_temp"] = round(current_temp, 2)
            if current_temp > 8.0:
                damage_factor = (current_temp - 8.0) * config.interaction_coefficients.get("spoilage_multiplier", 1.5) * dt
                new_metrics["payload_decay_index"] = min(100.0, new_metrics.get("payload_decay_index", 0.0) + damage_factor)
            else:
                new_metrics["payload_decay_index"] = max(0.0, new_metrics.get("payload_decay_index", 0.0) - 0.05 * dt)

        elif s_id == "datacenter_symbiosis":
            load = new_metrics.get("computing_load_pct", 50.0)
            target_heat = 30.0 + (load * 0.5)
            heat_delta = (target_heat - new_metrics.get("coolant_heat_output", 40.0)) * config.decay_rates.get("heat_transfer", 0.1) * dt
            new_metrics["coolant_heat_output"] = round(new_metrics.get("coolant_heat_output", 40.0) + heat_delta, 2)
            current_heat = new_metrics["coolant_heat_output"]
            if current_heat > 55.0:
                evap_rate = (current_heat - 55.0) * 0.12 * dt
                new_metrics["soil_moisture"] = max(10.0, new_metrics.get("soil_moisture", 60.0) - evap_rate)
                new_metrics["greenhouse_humidity"] = max(20.0, new_metrics.get("greenhouse_humidity", 70.0) - evap_rate * 0.5)

        else: # Legacy Clinical Human ICU Track
            cortisol_decay = config.decay_rates.get("cortisol_clearance", 0.05)
            new_cortisol = new_metrics.get("endocrine_cortisol", 20.0) * math.exp(-cortisol_decay * dt)
            new_metrics["endocrine_cortisol"] = max(2.0, new_cortisol)
            hr_drive = (new_metrics["endocrine_cortisol"] - 5.0) * 1.5
            target_hr = config.base_targets.get("heart_rate", 70.0) + max(0.0, hr_drive)
            new_hr = new_metrics.get("heart_rate", 80.0) + (target_hr - new_metrics.get("heart_rate", 80.0)) * 0.1 * dt
            new_metrics["heart_rate"] = new_hr
            target_bp = 120.0 + (new_hr - 70.0) * 0.4
            new_metrics["blood_pressure_systolic"] = new_metrics.get("blood_pressure_systolic", 120.0) + (target_bp - new_metrics.get("blood_pressure_systolic", 120.0)) * 0.2 * dt

        for k in new_metrics:
            new_metrics[k] = round(new_metrics[k], 4)

        return SystemStateMatrix(timestamp_seq=current.timestamp_seq + 1, metrics=new_metrics, metadata=current.metadata)

# ==========================================
# SIMULATION CHRONO RUNTIME
# ==========================================
class UniversalDigitalTwinTimeline:
    def __init__(self, initial_state: SystemStateMatrix, config: SectorConfig, max_history: int = 2000):
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
            raise ValueError(f"Variable '{variable_name}' is invalid in this environment profile.")
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

current_sector = "icu_human"
timeline = UniversalDigitalTwinTimeline(
    initial_state=SystemStateMatrix(timestamp_seq=0, metrics=INITIAL_STATES[current_sector].copy()),
    config=SECTOR_REGISTRY[current_sector]
)
# ==========================================
# FILE: main.py - PART 4 OF 4
# ==========================================

# ==========================================
# CHRONO CONTROL MACHINE API ROUTERS
# ==========================================
@app.get("/health", tags=["Infrastructure"])
async def health_check():
    return {"status": "healthy", "engine": "Global-Matrix-Core"}

@app.post("/initialize-sector", tags=["Security Verification Gates"])
async def initialize_sector(sector_id: str = Body(..., embed=True), license_key: str = Body(..., embed=True)):
    global timeline, current_sector
    if license_key not in VALID_LICENSE_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or expired Enterprise License Token.")
    plan_id = VALID_LICENSE_KEYS[license_key]
    active_plan = SUBSCRIPTION_PLANS[plan_id]
    if sector_id not in active_plan.allowed_sectors:
        raise HTTPException(status_code=403, detail="Access Denied: Sector not provisioned under your plan tier profile.")
    if sector_id not in SECTOR_REGISTRY:
        raise HTTPException(status_code=400, detail="Target sector infrastructure mapping layout not found.")

    current_sector = sector_id
    timeline = UniversalDigitalTwinTimeline(
        initial_state=SystemStateMatrix(timestamp_seq=0, metrics=INITIAL_STATES[sector_id].copy()),
        config=SECTOR_REGISTRY[sector_id],
        max_history=active_plan.max_history_buffer
    )
    return {"message": f"Successfully provisioned environment for {sector_id}", "tier_active": active_plan.tier_name, "history_buffer_allocated": active_plan.max_history_buffer, "current_step": timeline.current_step}

@app.get("/telemetry", tags=["Simulation Controls"])
async def get_telemetry():
    return {"current_step": timeline.current_step, "sector": current_sector, "metrics": timeline.get_current_state().metrics}

@app.post("/step", tags=["Simulation Controls"])
async def process_step():
    return {"state": timeline.process_realtime_step(), "current_step": timeline.current_step}

@app.post("/poke", tags=["Simulation Controls"])
async def execute_poke(variable_name: str = Body(..., embed=True), value: float = Body(..., embed=True)):
    try:
        updated = timeline.poke_variable(variable_name, value)
        return {"state": updated, "current_step": timeline.current_step}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rewind", tags=["Simulation Controls"])
async def rewind_timeline(steps: int = Body(..., embed=True)):
    return {"state": timeline.rewind(steps), "current_step": timeline.current_step}

@app.post("/fast-forward", tags=["Simulation Controls"])
async def fast_forward_timeline(minutes: float = Body(..., embed=True)):
    return {"state": timeline.fast_forward(minutes), "current_step": timeline.current_step}

# ==========================================
# REVENUE GENERATION GATEWAYS (Stripe B2B Matrix)
# ==========================================
@app.post("/billing/create-checkout-session", tags=["Monetization Strategy Channel"])
async def create_subscription_checkout(
    plan_id: str = Body(..., embed=True),
    success_url: str = Body("https://fly.dev", embed=True),
    cancel_url: str = Body("https://fly.dev", embed=True)
):
    if plan_id not in PLAN_PRICE_IDS:
        raise HTTPException(status_code=400, detail="Requested pricing package configuration does not exist.")
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': PLAN_PRICE_IDS[plan_id], 'quantity': 1}],
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"target_plan_allocation": plan_id}
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stripe Integration Disruption: {str(e)}")

@app.post("/billing/webhook", tags=["Monetization Strategy Channel"])
async def stripe_automated_webhook_listener(payload: bytes = Body(...), sig_header: str = Header(None, alias="Stripe-Signature")):
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Security verification failed.")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        target_plan = session.get("metadata", {}).get("target_plan_allocation")
        if target_plan in TIER_TOKENS:
            generated_key = TIER_TOKENS[target_plan]
            VALID_LICENSE_KEYS[generated_key] = target_plan
            print(f"🔒 TRANSACTION COMPLETE: Provisioned dynamic token -> {generated_key}")

    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
    
