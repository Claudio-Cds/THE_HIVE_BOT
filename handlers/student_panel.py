from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from handlers.management_handlers import (
    _apply_win,
    _apply_loss,
    _apply_aporte,
    _apply_saque,
    _get_last_result,
    _get_current_bank,
    _get_history,
)

from handlers.comprovantes import registrar_comprovante
from students import carregar_alunos
from config import load_config

cfg = load_config()
ADMIN_IDS = cfg.admin_ids


# ======================= TECLADO DO ALUNO ============================

def get_student_keyboard():
    keyboard = [
        ["🟢 Registrar WIN", "🔴 Registrar LOSS"],
        ["💵 Registrar Aporte", "💸 Registrar Saque"],
        ["📈 Minha banca atual", "📊 Meu último resultado"],
        ["📅 Meu histórico"],
        ["💳 Renovar plano"],
        ["📆 Status do meu plano", "📤 Enviar comprovante"],
        ["🛟 Suporte", "🧾 Meus dados"],
        ["❌ Fechar painel"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ======================= /painel_aluno ====================

async def painel_aluno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Painel do Aluno THE HIVE",
        reply_markup=get_student_keyboard(),
    )


# ======================= AÇÕES DOS BOTÕES ======================

async def aluno_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # WIN
    if text == "🟢 Registrar WIN":
        await update.message.reply_text("Envie o valor GANHO no dia:")
        context.user_data["action"] = "win"
        return

    # LOSS
    if text == "🔴 Registrar LOSS":
        await update.message.reply_text("Envie o valor PERDIDO no dia:")
        context.user_data["action"] = "loss"
        return

    # Aporte
    if text == "💵 Registrar Aporte":
        await update.message.reply_text("Envie o valor APORTADO:")
        context.user_data["action"] = "aporte"
        return

    # Saque
    if text == "💸 Registrar Saque":
        await update.message.reply_text("Envie o valor SACADO:")
        context.user_data["action"] = "saque"
        return

    # Banca atual
    if text == "📈 Minha banca atual":
        banca = _get_current_bank(user_id)
        return await update.message.reply_text(
            f"📈 Sua banca atual é: R$ {banca:.2f}"
        )

    # Último resultado
    if text == "📊 Meu último resultado":
        result = _get_last_result(user_id)
        if not result:
            return await update.message.reply_text("Nenhum registro encontrado ainda.")

        msg = (
            f"📊 Seu último dia:\n"
            f"• Data: {result['date']}\n"
            f"• Resultado: {result['status'].upper()}\n"
            f"• Banca final: R$ {result['banca_final']:.2f}"
        )
        return await update.message.reply_text(msg)

    # Histórico (últimos 10 registros)
    if text == "📅 Meu histórico":
        history = _get_history(user_id)
        if not history:
            return await update.message.reply_text("Nenhum histórico registrado.")

        linhas = []
        for r in history[-10:]:
            linhas.append(f"{r['date']} — {r['status']} — R$ {r['banca_final']:.2f}")

        return await update.message.reply_text("📅 Seus últimos registros:\n" + "\n".join(linhas))

    # Renovar plano
    if text == "💳 Renovar plano":
        return await update.message.reply_text(
            "💳 Para renovar seu plano, envie o PIX para a chave:\n\n"
            "`fe683628-858a-42ee-8444-884d49ff18a7`\n\n"
            "Depois clique em 📤 Enviar comprovante.",
            parse_mode="Markdown"
        )

    # Status do plano
    if text == "📆 Status do meu plano":
        alunos = carregar_alunos()
        aluno = alunos.get(str(user_id))

        if not aluno:
            return await update.message.reply_text("Você não possui cadastro.")

        msg = (
            "📆 *Status da sua assinatura*\n"
            f"• Status: {aluno.get('status')}\n"
            f"• Vencimento: {aluno.get('data_expira')}"
        )
        return await update.message.reply_text(msg, parse_mode="Markdown")

    # Enviar comprovante
    if text == "📤 Enviar comprovante":
        context.user_data["action"] = "comprovante"
        return await update.message.reply_text("📤 Envie o comprovante agora.")

    # Suporte
    if text == "🛟 Suporte":
        return await update.message.reply_text("🛟 Suporte THE HIVE: @Beekeepeersuporte")

    # Meus dados
    if text == "🧾 Meus dados":
        alunos = carregar_alunos()
        aluno = alunos.get(str(user_id))
        if not aluno:
            return await update.message.reply_text("Você não possui cadastro.")

        msg = (
            "🧾 *Seus dados*\n"
            f"• Nome: {aluno.get('nome')}\n"
            f"• ID: {user_id}\n"
            f"• Plano: {aluno.get('plano')}\n"
            f"• Status: {aluno.get('status')}\n"
            f"• Vencimento: {aluno.get('data_expira')}"
        )
        return await update.message.reply_text(msg, parse_mode="Markdown")

    # Fechar
    if text == "❌ Fechar painel":
        return await update.message.reply_text("Painel fechado.", reply_markup=ReplyKeyboardRemove())


# ======================= RECEBER VALORES / COMPROVANTE ======================

async def receber_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "action" not in context.user_data:
        return

    user_id = update.effective_user.id
    action = context.user_data["action"]

    # Comprovante
    if action == "comprovante":
        file_id = None
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
        elif update.message.document:
            file_id = update.message.document.file_id

        if not file_id:
            return await update.message.reply_text("Envie uma foto ou arquivo válido.")

        registrar_comprovante(user_id, file_id)

        context.user_data.clear()
        return await update.message.reply_text("📤 Comprovante recebido! Aguarde aprovação.")

    # Valores
    try:
        valor = float(update.message.text.replace(",", "."))
    except:
        return await update.message.reply_text("Digite apenas números.")

    if action == "win":
        msg = _apply_win(user_id, valor)
    elif action == "loss":
        msg = _apply_loss(user_id, valor)
    elif action == "aporte":
        msg = _apply_aporte(user_id, valor)
    elif action == "saque":
        msg = _apply_saque(user_id, valor)
    else:
        msg = "Ação desconhecida."

    context.user_data.clear()
    await update.message.reply_text(msg)


# ======================= EXPORTAR HANDLERS ======================

def get_student_panel_handlers():
    return [
        CommandHandler("painel_aluno", painel_aluno),

        # Botões
        MessageHandler(
            filters.Regex(
                r"^(🟢 Registrar WIN|🔴 Registrar LOSS|💵 Registrar Aporte|💸 Registrar Saque|📈 Minha banca atual|📊 Meu último resultado|📅 Meu histórico|💳 Renovar plano|📆 Status do meu plano|📤 Enviar comprovante|🛟 Suporte|🧾 Meus dados|❌ Fechar painel)$"
            ),
            aluno_buttons
        ),

        # Fotos e documentos → comprovantes
        MessageHandler(filters.PHOTO | filters.Document.ALL, receber_valor),

        # Somente valores numéricos
        MessageHandler(filters.TEXT & ~filters.COMMAND, receber_valor),
    ]
