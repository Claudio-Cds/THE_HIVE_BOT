from __future__ import annotations

from typing import Optional
from models import UserProfile
import storage


def get_or_create_user(user_id: int, name: Optional[str], username: Optional[str]) -> UserProfile:
    """
    Retorna o usuário se existir; caso contrário cria um novo.
    """
    user = storage.get_user(user_id)

    # Criar usuário novo
    if user is None:
        user = UserProfile(
            user_id=user_id,
            name=name,
            username=username,
            plan="free",
            discount_30_active=True,
        )
        storage.save_user(user)
        return user

    # Atualizar dados se mudaram
    updated = False

    if name and user.name != name:
        user.name = name
        updated = True

    if username and user.username != username:
        user.username = username
        updated = True

    if updated:
        storage.save_user(user)

    return user


def set_user_plan(user_id: int, plan: str) -> Optional[UserProfile]:
    """
    Altera o plano do usuário: free, vip, copy_only, vip_plus_copy.
    """
    user = storage.get_user(user_id)
    if not user:
        return None

    user.plan = plan
    storage.save_user(user)
    return user

