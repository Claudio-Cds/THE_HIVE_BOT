import os
import json
import importlib
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import load_config

cfg = load_config()
ADMIN_IDS = cfg.admin_ids

# Diretório raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ------------------------- LISTA DE MÓDULOS -------------------------

MODULES = [
    "bot",
    "config",
    "students",
    "storage",
    "keyboards",
    "models",
    "handlers.common",
    "handlers.admin",
    "handlers.management_handlers",
    "handlers.student_panel",
    "handlers.admin_panel",
    "handlers.admin_payments",
    "handlers.signals",
    "handlers.diagnostico",
]


# ------------------------- CHECAR IMPORTS ---------------------------

def check_modules():
    results = []
    for module in MODULES:
        try:
            importlib.import_module(module)
            results.append(f"[OK] {module}")
        except Exception as e:
            results.append(f"[ERRO] {module} → {str(e)}")
    return "\n".join(results)


# ------------------------- CHECAR ARQUIVOS --------------------------

REQUIRED_FILES = [
    ("requirements.txt", "requirements.txt"),
    ("students.json", os.path.join("data", "students.json")),
]

def check_files_and_sizes():
    results = []

    for label, rel_path in REQUIRED_FILES:
        path = os.path.join(ROOT_DIR, rel_path)

        if os.path.exists(path):
            size = os.path.getsize(path)
            if size == 0:
                results.append(f"[ALERTA] {label} — encontrado mas está VAZIO")
            else:
                results.append(f"[OK] {label} — {size} bytes")
        else:
            results.append(f"[ERRO] {label} — NÃO encontrado ({rel_path})")

    return "\n".join(results)


# ---------------------- BACKUP + AUTO-REPARO --------------------------

def backup_and_check_students_json():
    data_dir = os.path.join(ROOT_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    students_path = os.path.join(data_dir, "students.json")
    backup_dir = os.path.join(data_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    # Backup
    if os.path.exists(students_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"students_{timestamp}.bak")

        with open(students_path, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())

        backup_msg = f"[OK] Backup criado: data/backups/students_{timestamp}.bak"
    else:
        # Cria arquivo inicial
        with open(students_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        return "[ALERTA] students.json não existia e foi criado automaticamente."

    # Checar integridade
    try:
        with open(students_path, "r", encoding="utf-8") as f:
            json.load(f)
        return backup_msg + "\n[OK] students.json íntegro"
    except:
        with open(students_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        return backup_msg + "\n[ERRO] Arquivo corrompido → Recriado automaticamente."


# ---------------------- HANDLERS DUPLICADOS --------------------------

def check_handler_duplication():
    try:
        import handlers.student_panel as sp
        handlers = sp.get_student_panel_handlers()

        seen = set()
        duplicates = []

        for h in handlers:
            hname = str(h)
            if hname in seen:
                duplicates.append(hname)
            seen.add(hname)

        if duplicates:
            return "[ERRO] Handlers duplicados:\n" + "\n".join(duplicates)

        return "[OK] Nenhum handler duplicado"

    except Exception as e:
        return f"[ERRO] Falha ao verificar duplicações → {e}"


# ---------------------- FILTROS PERIGOSOS --------------------------

def check_dangerous_filters():
    handlers_dir = os.path.join(ROOT_DIR, "handlers")
    found = []

    for root, _, files in os.walk(handlers_dir):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)

                # IGNORA O PRÓPRIO ARQUIVO diagnostico.py
                if "diagnostico.py" in path:
                    continue

                with open(path, "r", encoding="utf-8") as fh:
                    code = fh.read()
                    if "filters.ALL" in code:
                        found.append(os.path.relpath(path, ROOT_DIR))

    if found:
        return "Filtros perigosos detectados:\n" + "\n".join(found)

    return "[OK] Nenhum filters.ALL encontrado"


# ---------------------- CHECAR /pendentes --------------------------

def check_pendentes_handler():
    try:
        import handlers.admin_payments as ap
        handlers = ap.get_admin_payment_handlers()

        for h in handlers:
            if "pendentes" in str(h):
                return "[OK] /pendentes registrado"

        return "[ERRO] /pendentes NÃO encontrado"

    except Exception as e:
        return f"[ERRO] Falha ao analisar /pendentes → {e}"


# ---------------------- TELEGRAM API --------------------------

async def check_telegram_api(bot):
    try:
        me = await bot.get_me()
        return f"[OK] Telegram API OK — @{me.username}"
    except Exception as e:
        return f"[ERRO] Telegram API → {str(e)}"


# ---------------------- SALVAR RELATÓRIO --------------------------

def save_report(report_text: str):
    diag_dir = os.path.join(ROOT_DIR, "data", "diagnostics")
    os.makedirs(diag_dir, exist_ok=True)

    filename = datetime.now().strftime("diagnostico_%Y%m%d_%H%M%S.txt")
    path = os.path.join(diag_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)

    return path


# ---------------------- /diagnostico --------------------------

async def diagnostico(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("Acesso negado.")

    header = (
        "PAINEL DE DIAGNÓSTICO — THE HIVE\n"
        f"{datetime.now()}\n\n"
    )

    report = header
    report += "### Módulos ###\n" + check_modules() + "\n\n"
    report += "### Arquivos ###\n" + check_files_and_sizes() + "\n\n"
    report += "### Students.json ###\n" + backup_and_check_students_json() + "\n\n"
    report += "### Handlers duplicados ###\n" + check_handler_duplication() + "\n\n"
    report += "### Filtros perigosos ###\n" + check_dangerous_filters() + "\n\n"
    report += "### /pendentes ###\n" + check_pendentes_handler() + "\n\n"

    # Notifica que vai enviar o arquivo
    await update.message.reply_text("📤 Gerando e enviando relatório...", parse_mode=None)

    # Teste da API Telegram
    api_status = await check_telegram_api(context.bot)
    report += "### Telegram API ###\n" + api_status + "\n\n"

    # Salvar como TXT
    path = save_report(report)

    # Enviar o relatório
    try:
        with open(path, "rb") as f:
            await context.bot.send_document(
                chat_id=update.effective_user.id,
                document=f,
                filename=os.path.basename(path),
                caption="📋 Relatório completo do diagnóstico.",
            )
    except:
        await update.message.reply_text("Erro ao enviar relatório, mas foi salvo.")


# ---------------------- EXPORTAR --------------------------

def get_diagnostic_handlers():
    return [
        CommandHandler("diagnostico", diagnostico)
    ]
