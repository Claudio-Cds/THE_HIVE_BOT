from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import load_config
from services.payments import activate_vip_for_user


cfg = load_config()


def is_admin(user_id: int) -> bool:
    return user_id in cfg.admin_ids


async def adm_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not is_admin(user.id):
        return

    if update.message:
        await update.message.reply_text(
            "Painel ADM THE HIVE.\n"
            "Comandos principais:\n"
            "/addvip <user_id> - Ativar VIP para um aluno\n"
            "/sinal ...        - Enviar sinal para VIP/FREE",
        )


async def adm_activate_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not is_admin(user.id):
        return

    if not context.args:
        if update.message:
            await update.message.reply_text("Uso: /addvip <user_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        if update.message:
            await update.message.reply_text("ID inválido.")
        return

    profile = activate_vip_for_user(target_id)
    if profile:
        if update.message:
            await update.message.reply_text(f"VIP ativado para o usuário {target_id}.")
    else:
        if update.message:
            await update.message.reply_text("Usuário não encontrado no sistema.")


def get_admin_handlers():
    return [
        CommandHandler("adm", adm_panel),
        CommandHandler("addvip", adm_activate_vip),
    ]
