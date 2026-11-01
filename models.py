# ==========================================
# FILE: models.py
# ==========================================
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class SystemStateMatrix(BaseModel):
    """
    Unified, sector-agnostic snapshot tracking an asset or environment's 
    variables at a discrete interval in simulated time.
    """
    timestamp_seq: int = Field(..., description="Sequential simulation frame index")
    metrics: Dict[str, float] = Field(..., description="Dynamic key-value array for variable parameters")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Context definitions (e.g. tracking identifiers)")

class SectorConfig(BaseModel):
    """
    Maps decay profiles, homeostatic target points, and kinetic modifiers 
    across different industrial operation configurations.
    """
    sector_id: str  # "icu_human", "aquaculture", "bio_logistics", "datacenter_symbiosis"
    base_targets: Dict[str, float]
    decay_rates: Dict[str, float]
    interaction_coefficients: Dict[str, float]
