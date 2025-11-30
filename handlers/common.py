
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from config import load_config
from .admin_panel import painel as painel_adm
from .student_panel import painel_aluno

cfg = load_config()
ADMIN_IDS = cfg.admin_ids


# ====================== /start =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Se for ADM -> mostra teclado para escolher o modo
    if user_id in ADMIN_IDS:
        keyboard = [
            ["👑 Modo ADM", "🎓 Modo Aluno"],
        ]
        await update.message.reply_text(
            "🐝 BEM-VINDO AO THE HIVE\n\n"
            "Você está logado como *Administrador*.\n\n"
            "Escolha abaixo em qual painel deseja entrar:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard, resize_keyboard=True, one_time_keyboard=False
            ),
            parse_mode="Markdown"
        )
    else:
        # Aluno comum -> vai para o painel do aluno
        await update.message.reply_text(
            "🐝 BEM-VINDO AO THE HIVE — Painel do aluno.",
        )
        # Abre o painel do aluno
        await painel_aluno(update, context)


# ====================== /id =======================

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🔍 Seu ID Telegram é:\n\n`{user.id}`",
        parse_mode="Markdown"
    )


# ====================== BOTÕES DE PERFIL (ADM) =======================

async def profile_switch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    text = update.message.text

    # Só o ADM pode ver esses botões
    if user_id not in ADMIN_IDS:
        return

    # Modo ADM
    if text == "👑 Modo ADM":
        # Remove teclado do perfil e abre o painel ADM
        await update.message.reply_text(
            "🔐 Entrando no *Painel do Administrador*...",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await painel_adm(update, context)
        return

    # Modo Aluno
    if text == "🎓 Modo Aluno":
        await update.message.reply_text(
            "🎓 Entrando no *Painel do Aluno*...",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await painel_aluno(update, context)
        return


# ====================== EXPORTAR HANDLERS =======================

def get_common_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("id", show_id),

        # Handler para os botões de perfil (apenas ADM)
        MessageHandler(
            filters.Regex("^(👑 Modo ADM|🎓 Modo Aluno)$"),
            profile_switch
        ),
    ]
