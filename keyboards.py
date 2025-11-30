from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# ------------------------------
# TECLADO INICIAL DO FREE
# ------------------------------

def free_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Benefícios do VIP", callback_data="free_beneficios_vip")],
        [InlineKeyboardButton("🔥 Ativar VIP com Desconto", callback_data="free_ativar_vip")],
        [InlineKeyboardButton("📊 Como funciona o gerenciamento?", callback_data="free_info_gerenciamento")]
    ])


# ------------------------------
# TECLADO INICIAL DO VIP
# ------------------------------

def vip_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Abrir gerenciamento diário", callback_data="vip_abrir_gerenciamento")],
        [InlineKeyboardButton("📁 Histórico completo", callback_data="vip_historico")],
        [InlineKeyboardButton("⚙️ Configurações do VIP", callback_data="vip_config")],
    ])


# ------------------------------
# CONFIRMAÇÃO DE ATIVAÇÃO VIP
# ------------------------------

def vip_confirm_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✔️ Confirmar Pagamento", callback_data="vip_confirmar_pagamento")],
        [InlineKeyboardButton("📄 Ver Políticas de Acesso", callback_data="vip_politicas")],
    ])


# ------------------------------
# TECLADO DO ADM (sessão de sinais)
# ------------------------------

def admin_session_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟦 Sessão FREE", callback_data="adm_sessao_free"),
            InlineKeyboardButton("🟨 Sessão VIP", callback_data="adm_sessao_vip"),
        ],
        [InlineKeyboardButton("🟣 Sessão AMBOS", callback_data="adm_sessao_ambos")]
    ])


# ------------------------------
# TECLADO DO GERENCIAMENTO
# ------------------------------

def gerenciamento_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Registrar WIN", callback_data="mgmt_win"),
            InlineKeyboardButton("Registrar STOP", callback_data="mgmt_stop")
        ],
        [InlineKeyboardButton("📊 Ver Resultados", callback_data="mgmt_resultados")]
    ])


# ------------------------------
# TECLADO DE ESCOLHA DE PLANO
# ------------------------------

def planos_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("R$ 149,99 → VIP 30 dias", callback_data="ativar_plano_vip")],
        [InlineKeyboardButton("R$ 209,00 → VIP + Copy Trader", callback_data="ativar_plano_combo")],
        [InlineKeyboardButton("R$ 179,00 → Copy Trader Indep.", callback_data="ativar_plano_copy")]
    ])
