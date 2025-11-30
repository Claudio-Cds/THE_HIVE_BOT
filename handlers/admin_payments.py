from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from handlers.comprovantes import listar_pendentes, aprovar_comprovante, rejeitar_comprovante
from students import renovar_plano, verificar_status, carregar_alunos

from config import load_config

cfg = load_config()
ADMIN_IDS = cfg.admin_ids


# ===================== /pendentes (ADM) =====================

async def cmd_pendentes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return await update.message.reply_text("Apenas o ADM pode usar este comando.")

    pendentes = listar_pendentes()

    if not pendentes:
        return await update.message.reply_text("Nenhum comprovante pendente.")

    for aluno_id, dados in pendentes.items():
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✔ Aprovar", callback_data=f"aprovar_{aluno_id}"),
                InlineKeyboardButton("❌ Rejeitar", callback_data=f"rejeitar_{aluno_id}"),
            ]
        ])

        await update.message.reply_text(
            f"📤 Comprovante pendente\nAluno ID: {aluno_id}\nData: {dados['date']}",
            reply_markup=keyboard,
        )

        # tenta enviar também o arquivo do comprovante
        try:
            await context.bot.send_photo(
                chat_id=user_id,
                photo=dados["file_id"],
                caption=f"Comprovante do aluno {aluno_id}",
            )
        except Exception:
            pass


# ===================== CALLBACK DE APROVAÇÃO =====================

async def aprovacao_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("aprovar_"):
        aluno_id = data.split("_")[1]
        uid = int(aluno_id)

        ok = aprovar_comprovante(uid)
        if not ok:
            return await query.edit_message_text("Erro ao aprovar comprovante.")

        # renova plano por +30 dias
        renovar_plano(uid, 30)

        await query.edit_message_text(f"✔ Comprovante de {aluno_id} APROVADO.")

        # notifica aluno
        try:
            await context.bot.send_message(
                uid,
                "✅ Seu pagamento foi aprovado! Seu plano foi renovado por mais 30 dias."
            )
        except Exception:
            pass

    elif data.startswith("rejeitar_"):
        aluno_id = data.split("_")[1]
        uid = int(aluno_id)

        ok = rejeitar_comprovante(uid)
        if not ok:
            return await query.edit_message_text("Erro ao rejeitar comprovante.")

        await query.edit_message_text(f"❌ Comprovante de {aluno_id} REJEITADO.")

        try:
            await context.bot.send_message(
                uid,
                "❌ Seu comprovante foi analisado e REJEITADO. "
                "Verifique os dados e envie novamente."
            )
        except Exception:
            pass


def get_admin_payment_handlers():
    return [
        CommandHandler("pendentes", cmd_pendentes),
        CallbackQueryHandler(aprovacao_callback),
    ]
