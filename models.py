from dataclasses import dataclass, field
from typing import Optional, Literal
import datetime

UserPlanType = Literal["free", "vip", "copy_only", "vip_plus_copy"]

@dataclass
class UserProfile:
    user_id: int
    name: str | None = None
    username: str | None = None
    plan: UserPlanType = "free"
    vip_valid_until: Optional[str] = None
    copy_valid_until: Optional[str] = None
    is_blocked: bool = False
    discount_30_active: bool = True
    discount_5_active: bool = False
    discount_50_active: bool = False
    months_paid_consecutive: int = 0
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

@dataclass
class ManagementState:
    user_id: int
    initial_bank: float
    current_bank: float
    profile: Literal["conservative", "aggressive"] = "conservative"
    copy_profile_locked: bool = False
    cycle_day: int = 1
    positive_days: int = 0
    negative_days: int = 0
    total_gain_percent: float = 0.0
    total_loss_percent: float = 0.0

@dataclass
class SignalRecord:
    id: int
    pair: str
    expiry: str
    direction: str
    entry_time: str
    valid_minutes: int = 5
    group_type: Literal["free", "vip", "both"] = "vip"
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    result: Optional[str] = None
