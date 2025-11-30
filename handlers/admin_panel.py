from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from config import load_config
from students import (
    carregar_alunos,
    salvar_alunos,
    renovar_plano,
    verificar_status,
)

cfg = load_config()
ADMIN_IDS = cfg.admin_ids


# ====================== PAINEL ADM =======================

async def painel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("Apenas o ADM pode acessar o painel.")

    keyboard = [
        ["👥 Lista de alunos"],
        ["🔄 Renovar plano"],
        ["⏳ Ver status de um aluno"],
        ["⛔ Bloquear aluno", "✔ Liberar aluno"],
        ["❌ Fechar painel"],
    ]

    await update.message.reply_text(
        "📋 Painel do Administrador THE HIVE",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=False
        )
    )


# ====================== MENU CLIQUES =======================

async def menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    text = update.message.text

    if text == "👥 Lista de alunos":
        alunos = carregar_alunos()
        if not alunos:
            return await update.message.reply_text("Nenhum aluno registrado.")

        lista = "👥 *Lista de Alunos Registrados*\n\n"
        for uid, a in alunos.items():
            lista += f"• ID: `{uid}` — Status: *{a.get('status', 'desconhecido')}*\n"

        return await update.message.reply_text(lista, parse_mode="Markdown")

    if text == "🔄 Renovar plano":
        return await update.message.reply_text("Use:\n/adm_renovar ID dias")

    if text == "⏳ Ver status de um aluno":
        return await update.message.reply_text("Use:\n/adm_status ID")

    if text == "⛔ Bloquear aluno":
        return await update.message.reply_text("Use:\n/adm_bloquear ID")

    if text == "✔ Liberar aluno":
        return await update.message.reply_text("Use:\n/adm_liberar ID")

    if text == "❌ Fechar painel":
        return await update.message.reply_text(
            "Painel fechado.",
            reply_markup=ReplyKeyboardRemove()
        )


# ====================== COMANDOS =======================

async def adm_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, uid = update.message.text.split()
        estado = verificar_status(int(uid))
        await update.message.reply_text(f"Status do aluno {uid}: {estado}")
    except:
        await update.message.reply_text("Use:\n/adm_status ID")


async def adm_renovar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, uid, dias = update.message.text.split()
        renovar_plano(int(uid), int(dias))
        await update.message.reply_text(f"Plano renovado para o aluno {uid} por {dias} dias.")
    except:
        await update.message.reply_text("Use:\n/adm_renovar ID dias")


async def adm_bloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, uid = update.message.text.split()

        alunos = carregar_alunos()
        if uid not in alunos:
            return await update.message.reply_text("Aluno não encontrado.")

        alunos[uid]["status"] = "bloqueado"
        salvar_alunos(alunos)

        await update.message.reply_text(f"Aluno {uid} BLOQUEADO.")
    except:
        await update.message.reply_text("Use:\n/adm_bloquear ID")


async def adm_liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        _, uid = update.message.text.split()

        alunos = carregar_alunos()
        if uid not in alunos:
            return await update.message.reply_text("Aluno não encontrado.")

        alunos[uid]["status"] = "ativo"
        salvar_alunos(alunos)

        await update.message.reply_text(f"Aluno {uid} LIBERADO.")
    except:
        await update.message.reply_text("Use:\n/adm_liberar ID")


# ====================== EXPORTAR HANDLERS =======================

def get_admin_panel_handlers():
    return [
        CommandHandler("painel", painel),

        # CORRIGIDO: agora só recebe CLIQUES DO MENU REAL,
        # e não bloqueia mais nenhum comando do bot.
        MessageHandler(
            filters.Regex(
                "^(👥 Lista de alunos|🔄 Renovar plano|⏳ Ver status de um aluno|⛔ Bloquear aluno|✔ Liberar aluno|❌ Fechar painel)$"
            ),
            menu_click
        ),

        CommandHandler("adm_status", adm_status),
        CommandHandler("adm_renovar", adm_renovar),
        CommandHandler("adm_bloquear", adm_bloquear),
        CommandHandler("adm_liberar", adm_liberar),
    ]
