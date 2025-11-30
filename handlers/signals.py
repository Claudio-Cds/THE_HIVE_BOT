from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters

from config import load_config
from services.signals import register_signal


cfg = load_config()


def is_admin(user_id: int) -> bool:
    return user_id in cfg.admin_ids


async def send_signal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Uso: /sinal <par> <hora_minuto> <CALL|PUT> <free|vip|both>
    Ex: /sinal EURUSD 14:20 PUT vip
    """
    user = update.effective_user
    if not user or not is_admin(user.id):
        return

    if len(context.args) < 4:
        if update.message:
            await update.message.reply_text(
                "Uso: /sinal <par> <hora> <CALL|PUT> <free|vip|both>"
            )
        return

    pair = context.args[0]
    entry_time = context.args[1]
    direction = context.args[2]
    group_type = context.args[3]

    rec = register_signal(pair, entry_time, direction, group_type)

    text = (
        "🐝 SINAL — THE HIVE\n"
        f"PAR: {rec['pair']}\n"
        f"EXPIRAÇÃO: {rec['expiry']}\n"
        f"DIREÇÃO: {rec['direction']}\n"
        f"ENTRADA: {rec['entry_time']}\n"
        f"VALIDADE: {rec['valid_minutes']} MINUTOS\n"
        "Observação: Siga o gerenciamento."
    )

    group_vip_id = context.bot_data.get("GROUP_VIP_ID")
    group_free_id = context.bot_data.get("GROUP_FREE_ID")

    if group_type in ("vip", "both") and group_vip_id:
        await context.bot.send_message(chat_id=group_vip_id, text=text)

    if group_type in ("free", "both") and group_free_id:
        await context.bot.send_message(chat_id=group_free_id, text=text)

    if update.message:
        await update.message.reply_text(f"Sinal enviado para: {group_type.upper()}")


async def set_group_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not chat:
        return

    context.bot_data["GROUP_VIP_ID"] = chat.id

    if update.message:
        await update.message.reply_text(f"Grupo VIP registrado com ID {chat.id}.")


async def set_group_free(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not chat:
        return

    context.bot_data["GROUP_FREE_ID"] = chat.id

    if update.message:
        await update.message.reply_text(f"Grupo FREE registrado com ID {chat.id}.")


def get_signal_handlers():
    return [
        CommandHandler(
            "sinal",
            send_signal_cmd,
            filters=filters.ChatType.GROUPS | filters.ChatType.PRIVATE,
        ),
        CommandHandler(
            "set_group_vip",
            set_group_vip,
            filters=filters.ChatType.GROUPS,
        ),
        CommandHandler(
            "set_group_free",
            set_group_free,
            filters=filters.ChatType.GROUPS,
        ),
    ]

