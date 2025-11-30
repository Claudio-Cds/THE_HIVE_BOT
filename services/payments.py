from datetime import datetime, timedelta
from typing import Optional
from models import UserProfile
import storage


def _now_utc() -> datetime:
    return datetime.utcnow()


def activate_vip_for_user(
    user_id: int,
    days: int = 30,
    tolerance_days: int = 5,
) -> Optional[UserProfile]:
    """
    Ativa plano VIP para o usuário:
    - days: dias de acesso oficial
    - tolerance_days: dias extras (tolerância) após o vencimento
    """
    user = storage.get_user(user_id)
    if not user:
        return None

    now = _now_utc()
    valid_until = now + timedelta(days=days + tolerance_days)

    user.plan = "vip"
    user.vip_valid_until = valid_until.isoformat()

    # Já usou o desconto inicial de 30%
    user.discount_30_active = False

    # Controle simples de fidelidade (pode ser expandido depois)
    user.months_paid_consecutive += 1

    storage.save_user(user)
    return user


def activate_copy_only_for_user(
    user_id: int,
    days: int = 30,
) -> Optional[UserProfile]:
    """
    Ativa plano SOMENTE COPY (R$ 179,00):
    - sem VIP
    - com gerenciamento liberado, mas perfil conservador
    """
    user = storage.get_user(user_id)
    if not user:
        return None

    now = _now_utc()
    valid_until = now + timedelta(days=days)

    user.plan = "copy_only"
    user.copy_valid_until = valid_until.isoformat()

    storage.save_user(user)
    return user


def activate_vip_plus_copy_for_user(
    user_id: int,
    days: int = 30,
    tolerance_days: int = 5,
) -> Optional[UserProfile]:
    """
    Ativa VIP + COPY junto (combo):
    - mesmo período de validade para ambos
    """
    user = storage.get_user(user_id)
    if not user:
        return None

    now = _now_utc()
    valid_until_vip = now + timedelta(days=days + tolerance_days)
    valid_until_copy = now + timedelta(days=days)

    user.plan = "vip_plus_copy"
    user.vip_valid_until = valid_until_vip.isoformat()
    user.copy_valid_until = valid_until_copy.isoformat()

    user.discount_30_active = False
    user.months_paid_consecutive += 1

    storage.save_user(user)
    return user
