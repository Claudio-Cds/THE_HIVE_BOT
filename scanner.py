import os
import importlib
import traceback

print("=== VARREDURA THE HIVE BOT ===\n")

PROJECT = "C:\\Users\\Alex\\Desktop\\THE_HIVE_BOT"

modules = [
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
]

def test_import(module):
    try:
        importlib.import_module(module)
        print(f"[✔] Importado com sucesso: {module}")
    except Exception as e:
        print(f"[❌] ERRO ao importar: {module}")
        print("     ", e)
        print(traceback.format_exc())

# Listar arquivos do projeto
print("Arquivos encontrados no projeto:\n")
for root, dirs, files in os.walk(PROJECT):
    for f in files:
        if f.endswith(".py"):
            print(" -", os.path.join(root, f))

print("\nTestando imports:\n")
for m in modules:
    test_import(m)
