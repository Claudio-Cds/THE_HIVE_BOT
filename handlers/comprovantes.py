import os
import json
from datetime import datetime

COMPROVANTES_FILE = os.path.join("data", "comprovantes.json")


def _load_comprovantes():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(COMPROVANTES_FILE):
        with open(COMPROVANTES_FILE, "w", encoding="utf-8") as f:
            f.write("{}")

    with open(COMPROVANTES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


def _save_comprovantes(data: dict):
    with open(COMPROVANTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def registrar_comprovante(user_id: int, file_id: str):
    data = _load_comprovantes()

    data[str(user_id)] = {
        "file_id": file_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "pendente"
    }

    _save_comprovantes(data)


def listar_pendentes():
    data = _load_comprovantes()
    return {k: v for k, v in data.items() if v.get("status") == "pendente"}


def aprovar_comprovante(user_id: int):
    data = _load_comprovantes()
    if str(user_id) not in data:
        return False

    data[str(user_id)]["status"] = "aprovado"
    _save_comprovantes(data)
    return True


def rejeitar_comprovante(user_id: int):
    data = _load_comprovantes()
    if str(user_id) not in data:
        return False

    data[str(user_id)]["status"] = "rejeitado"
    _save_comprovantes(data)
    return True
