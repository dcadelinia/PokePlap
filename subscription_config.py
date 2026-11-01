# ==========================================
# FILE: subscription_config.py
# ==========================================
from pydantic import BaseModel, Field
from typing import Dict, List

class SubscriptionTier(BaseModel):
    tier_name: str  # "Free_Trial", "Professional", "Enterprise_Scale"
    allowed_sectors: List[str]
    max_history_buffer: int
    allow_custom_pokes: bool
    rate_limit_ff_mins: float

# Enterprise B2B SaaS Tiers Configuration
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
        rate_limit_ff_mins=1440.0 # 24 Hours continuous simulation jumps
    )
}

# In-Memory License Verification Key Database Map
VALID_LICENSE_KEYS: Dict[str, str] = {
    "SKU-CLINICAL-FREE-99": "plan_icu_basic",
    "SKU-AQUA-PRO-77X": "plan_agtech_pro",
    "SKU-GLOBAL-ENTERPRISE-DYNAMIC-MATRIX": "plan_global_matrix"
}
