from typing import Optional
from models import ManagementState
import storage


def init_management(user_id: int, initial_bank: float, profile: str = "conservative") -> ManagementState:
    """
    Cria um novo gerenciamento para o usuário.
    """
    mgmt = ManagementState(
        user_id=user_id,
        initial_bank=initial_bank,
        current_bank=initial_bank,
        profile=profile,
    )
    storage.save_management(mgmt)
    return mgmt


def get_or_create_management(user_id: int, initial_bank: float = 0.0) -> Optional[ManagementState]:
    """
    Retorna o gerenciamento do usuário; se não existir e tiver banco inicial, cria.
    """
    mgmt = storage.get_management(user_id)

    if mgmt is None and initial_bank > 0:
        mgmt = init_management(user_id, initial_bank=initial_bank)

    return mgmt


def update_after_day_result(user_id: int, new_bank: float, result: str) -> Optional[ManagementState]:
    """
    Atualiza gerenciamento de acordo com o resultado do dia:
    - result = "WIN", "STOP" ou "NEUTRO"
    """
    mgmt = storage.get_management(user_id)
    if not mgmt:
        return None

    old_bank = mgmt.current_bank
    mgmt.current_bank = new_bank

    # Porcentagem de alteração
    if old_bank > 0:
        delta_pct = ((new_bank - old_bank) / old_bank) * 100.0
    else:
        delta_pct = 0.0

    # Acumular estatísticas
    if delta_pct >= 0:
        mgmt.total_gain_percent += delta_pct
    else:
        mgmt.total_loss_percent += abs(delta_pct)

    # Dias positivos/negativos
    if result.upper() == "WIN":
        mgmt.positive_days += 1
    elif result.upper() == "STOP":
        mgmt.negative_days += 1

    # Avançar ciclo (1–30)
    if mgmt.cycle_day < 30:
        mgmt.cycle_day += 1
    else:
        mgmt.cycle_day = 1

    # Salvar alterações
    storage.save_management(mgmt)
    return mgmt
