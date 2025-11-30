from models import SignalRecord
import storage


def register_signal(pair: str, entry_time: str, direction: str, group_type: str = "vip") -> SignalRecord:
    """
    Registra um sinal no sistema THE HIVE.

    Parâmetros:
    - pair: exemplo "EURUSD"
    - entry_time: exemplo "14:20"
    - direction: "CALL" ou "PUT"
    - group_type: "free", "vip", "both"

    Retorna:
    - objeto SignalRecord salvo no arquivo signals.json
    """

    # Criar sinal
    rec = SignalRecord(
        id=0,                          # será definido no storage
        pair=pair.upper(),             # sempre em maiúsculas
        expiry="M5",                   # expiração fixa THE HIVE
        direction=direction.upper(),   # CALL / PUT
        entry_time=entry_time,         # horário da entrada
        valid_minutes=5,               # validade de 5 minutos
        group_type=group_type.lower(), # free / vip / both
    )

    # Salvar no storage
    storage.save_signal(rec)

    return rec


def update_signal_result(signal_id: int, result: str) -> None:
    """
    Atualiza o resultado de um sinal já salvo.
    result = "WIN" ou "LOSS"
    """
    storage.update_signal_result(signal_id, result.upper())

