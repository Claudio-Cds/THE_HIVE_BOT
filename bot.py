import logging
from telegram.ext import ApplicationBuilder, Application

from config import load_config

from handlers.common import get_common_handlers
from handlers.admin import get_admin_handlers
from handlers.management_handlers import get_management_handlers
from handlers.student_panel import get_student_panel_handlers
from handlers.admin_panel import get_admin_panel_handlers
from handlers.admin_payments import get_admin_payment_handlers
from handlers.diagnostico import get_diagnostic_handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def build_application() -> Application:
    cfg = load_config()
    app = ApplicationBuilder().token(cfg.token).build()

    # HANDLERS GERAIS
    for h in get_common_handlers():
        app.add_handler(h)

    # Painel ADM
    for h in get_admin_handlers():
        app.add_handler(h)

    # Painel ADM THE HIVE
    for h in get_admin_panel_handlers():
        app.add_handler(h)

    # Gerenciamento de banca
    for h in get_management_handlers():
        app.add_handler(h)

    # Painel do estudante
    for h in get_student_panel_handlers():
        app.add_handler(h)

    # Confirmar/comprovar pagamentos
    for h in get_admin_payment_handlers():
        app.add_handler(h)

    # PAINEL DE DIAGNÓSTICO AVANÇADO
    for h in get_diagnostic_handlers():
        app.add_handler(h)

    return app


def main() -> None:
    app = build_application()
    logger.info("🐝 BOT THE HIVE iniciado.")
    app.run_polling()


if __name__ == "__main__":
    main()
