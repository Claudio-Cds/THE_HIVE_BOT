import os
import json
from datetime import datetime, timedelta

STUDENTS_FILE = os.path.join("data", "students.json")


# ====================== CARREGAR ALUNOS =======================

def carregar_alunos():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
            f.write("{}")

    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}


# ====================== SALVAR ALUNOS =======================

def salvar_alunos(data: dict):
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ====================== RENOVAR PLANO =======================

def renovar_plano(user_id: int, dias: int = 30):
    alunos = carregar_alunos()
    uid = str(user_id)

    nova_data = datetime.now() + timedelta(days=dias)

    if uid not in alunos:
        alunos[uid] = {}

    alunos[uid]["status"] = "ativo"
    alunos[uid]["plano"] = "vip"
    alunos[uid]["data_expira"] = nova_data.strftime("%Y-%m-%d")

    salvar_alunos(alunos)
    return True


# ====================== VERIFICAR STATUS =======================

def verificar_status(user_id: int):
    alunos = carregar_alunos()
    uid = str(user_id)

    if uid not in alunos:
        return "sem_registro"

    aluno = alunos[uid]
    data_expira = aluno.get("data_expira", None)

    if not data_expira:
        return "sem_validade"

    try:
        expira = datetime.strptime(data_expira, "%Y-%m-%d")
    except:
        return "data_invalida"

    if datetime.now() > expira:
        return "expirado"

    return "ativo"


# ====================== ADICIONAR ALUNO (ANTIGO PAINEL ADM) =======================

def adicionar_aluno(user_id: int, nome: str = "Aluno"):
    alunos = carregar_alunos()
    uid = str(user_id)

    alunos[uid] = {
        "nome": nome,
        "plano": "vip",
        "status": "ativo",
        "data_expira": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    }

    salvar_alunos(alunos)
    return True
