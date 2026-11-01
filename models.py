from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum 

class OrganizationType(str, Enum):
VETERINARY = "veterinary"
CLINICAL_HUMAN = "clinical_human"
CRO_RESEARCH = "cro_research"
HARDWARE_OEM = "hardware_oem" 

class SecurityRole(str, Enum):
PLATFORM_ADMIN = "platform_admin"
CLINICIAN = "clinician"
RESEARCHER = "researcher"
AUDITOR = "auditor" 

class TenantOrganization(BaseModel):
org_id: str = Field(..., description="Unique enterprise identifier UUID")
legal_name: str = Field(..., description="Registered legal name matching institutional records")
sector: OrganizationType
clearing_account_verified: bool = False
active_subscription_tier: str = "veta_tier"
created_at: datetime = Field(default_factory=datetime.utcnow) 

class InstitutionalUser(BaseModel):
user_id: str
org_id: str
email: EmailStr
display_name: str
assigned_role: SecurityRole
is_active: bool = True
cryptographic_signature_key: Optional[str] = None 

class PhysiologicalAuditLog(BaseModel):
log_id: str
user_id: str
org_id: str
timestamp: datetime = Field(default_factory=datetime.utcnow)
species_context: str
timeline_scrub_delta_seconds: int
hazard_index_observed: float
reversibility_status: str
governance_hash: str = Field(..., description="SHA256 fingerprint anchoring session parameters under WTO-TRIPS/TUTSA audit standards")
