import os
import json
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

MANAGEMENT_FILE = os.path.join("data", "management.json")


# ================= BASE DE DADOS DE GERENCIAMENTO =================

def _load_management():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(MANAGEMENT_FILE):
        with open(MANAGEMENT_FILE, "w", encoding="utf-8") as f:
            f.write("{}")

    with open(MANAGEMENT_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_management(data: dict):
    with open(MANAGEMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ================= FUNÇÕES DE BANCAS POR ALUNO ====================

def _get_current_bank(user_id: int) -> float:
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "banca_atual" not in data[uid]:
        return 0.0

    return float(data[uid]["banca_atual"])


def _add_initial_bank(user_id: int, value: float) -> str:
    data = _load_management()
    uid = str(user_id)

    if uid not in data:
        data[uid] = {}

    data[uid]["banca_atual"] = value

    if "historico" not in data[uid]:
        data[uid]["historico"] = []

    data[uid]["historico"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "banca_inicial",
        "banca_final": value,
    })

    _save_management(data)
    return f"✔ Sua banca inicial foi definida como R$ {value:.2f}"


def _apply_win(user_id: int, amount: float) -> str:
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "banca_atual" not in data[uid]:
        return "❗ Primeiro registre sua banca inicial usando: /banca valor"

    banca = float(data[uid]["banca_atual"])
    banca_nova = banca + amount
    data[uid]["banca_atual"] = banca_nova

    data[uid]["historico"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "win",
        "banca_final": banca_nova,
    })

    _save_management(data)

    return (
        f"🟢 WIN registrado!\n"
        f"Lucro: R$ {amount:.2f}\n"
        f"Nova banca: R$ {banca_nova:.2f}"
    )


def _apply_loss(user_id: int, amount: float) -> str:
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "banca_atual" not in data[uid]:
        return "❗ Primeiro registre sua banca inicial usando: /banca valor"

    banca = float(data[uid]["banca_atual"])
    banca_nova = banca - amount
    data[uid]["banca_atual"] = banca_nova

    data[uid]["historico"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "loss",
        "banca_final": banca_nova,
    })

    _save_management(data)

    return (
        f"🔴 LOSS registrado!\n"
        f"Perda: R$ {amount:.2f}\n"
        f"Nova banca: R$ {banca_nova:.2f}"
    )


def _apply_aporte(user_id: int, amount: float) -> str:
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "banca_atual" not in data[uid]:
        return "❗ Primeiro registre sua banca inicial usando: /banca valor"

    banca = float(data[uid]["banca_atual"])
    banca_nova = banca + amount
    data[uid]["banca_atual"] = banca_nova

    data[uid]["historico"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "aporte",
        "banca_final": banca_nova,
    })

    _save_management(data)

    return (
        f"💵 Aporte registrado!\n"
        f"Valor: R$ {amount:.2f}\n"
        f"Nova banca: R$ {banca_nova:.2f}"
    )


def _apply_saque(user_id: int, amount: float) -> str:
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "banca_atual" not in data[uid]:
        return "❗ Primeiro registre sua banca inicial usando: /banca valor"

    banca = float(data[uid]["banca_atual"])
    banca_nova = banca - amount
    data[uid]["banca_atual"] = banca_nova

    data[uid]["historico"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "saque",
        "banca_final": banca_nova,
    })

    _save_management(data)

    return (
        f"💸 Saque registrado!\n"
        f"Valor: R$ {amount:.2f}\n"
        f"Nova banca: R$ {banca_nova:.2f}"
    )


def _get_last_result(user_id: int):
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "historico" not in data[uid]:
        return None

    hist = data[uid]["historico"]
    if not hist:
        return None

    return hist[-1]


def _get_history(user_id: int):
    data = _load_management()
    uid = str(user_id)

    if uid not in data or "historico" not in data[uid]:
        return []

    return data[uid]["historico"]


# ==================== HANDLER /banca =======================

async def cmd_banca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Define a banca inicial do aluno:
    /banca 300
    """
    parts = update.message.text.split()

    if len(parts) != 2:
        return await update.message.reply_text("Uso correto: /banca 300")

    try:
        value = float(parts[1].replace(",", "."))
    except ValueError:
        return await update.message.reply_text("Valor inválido.")

    user_id = update.effective_user.id
    msg = _add_initial_bank(user_id, value)
    await update.message.reply_text(msg)


def get_management_handlers():
    return [
        CommandHandler("banca", cmd_banca),
    ]
