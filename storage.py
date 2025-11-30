import json
import os
from typing import Dict, Any, Optional, List
from models import UserProfile, ManagementState, SignalRecord

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
MGMT_FILE = os.path.join(DATA_DIR, "management.json")
SIGNALS_FILE = os.path.join(DATA_DIR, "signals.json")


# --------------------------
# JSON helpers
# --------------------------

def _load_json(path: str):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def _save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --------------------------
# USERS
# --------------------------

def get_user(user_id: int) -> Optional[UserProfile]:
    data = _load_json(USERS_FILE)
    raw = data.get(str(user_id))
    if not raw:
        return None
    return UserProfile(**raw)


def save_user(user: UserProfile) -> None:
    data = _load_json(USERS_FILE)
    data[str(user.user_id)] = user.__dict__
    _save_json(USERS_FILE, data)


def get_all_users() -> Dict[str, Any]:
    return _load_json(USERS_FILE)


# --------------------------
# MANAGEMENT
# --------------------------

def get_management(user_id: int) -> Optional[ManagementState]:
    data = _load_json(MGMT_FILE)
    raw = data.get(str(user_id))
    if not raw:
        return None
    return ManagementState(**raw)


def save_management(user_id: int, mgmt: ManagementState) -> None:
    data = _load_json(MGMT_FILE)
    data[str(user_id)] = mgmt.__dict__
    _save_json(MGMT_FILE, data)


# --------------------------
# SIGNALS
# --------------------------

def save_signal(record: SignalRecord) -> None:
    data = _load_json(SIGNALS_FILE)
    data[str(record.timestamp)] = record.__dict__
    _save_json(SIGNALS_FILE, data)


def load_signals() -> Dict[str, Any]:
    return _load_json(SIGNALS_FILE)