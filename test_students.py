from students import adicionar_aluno, verificar_status

print("=== TESTE MÓDULO DE ALUNOS THE HIVE ===")

adicionar_aluno(
    user_id=111222333,
    nome="Aluno Teste",
    plano="vip",
    dias=30
)

print("Aluno criado!")

status = verificar_status(111222333)
print("Status:", status)
