"""
==========================================================================
  TESTE DE INTEGRACAO REAL - API GERENCIADOR DE VAGAS
==========================================================================

  Este script faz requisicoes HTTP reais na API rodando no Docker.
  Ele insere, lista, busca, atualiza e deleta vagas DE VERDADE no banco.

  Pre-requisito: Docker rodando com 'docker-compose up --build'
  Para executar:  python tests/test_rotas.py

==========================================================================
"""

import requests
import sys
import time
from datetime import date

# URL base da API rodando no Docker
BASE_URL = "http://localhost:5000"

# Contadores de resultado
total_testes = 0
testes_ok = 0
testes_falha = 0
ids_criados = []  # Guarda IDs criados para limpar no final


def log(mensagem):
    """Imprime uma mensagem formatada no terminal."""
    print(f"  {mensagem}")


def separador(titulo=""):
    """Imprime um separador visual no terminal."""
    if titulo:
        print(f"\n{'='*65}")
        print(f"  {titulo}")
        print(f"{'='*65}")
    else:
        print(f"  {'-'*60}")


def registrar_resultado(nome_teste, passou, detalhes=""):
    """Registra o resultado de cada teste no terminal."""
    global total_testes, testes_ok, testes_falha
    total_testes += 1

    if passou:
        testes_ok += 1
        status = "[OK]"
    else:
        testes_falha += 1
        status = "[FALHOU]"

    print(f"  {status} {nome_teste}")
    if detalhes:
        print(f"         -> {detalhes}")


def verificar_api_online():
    """Verifica se a API esta acessivel antes de comecar os testes."""
    print("\n  Verificando se a API esta online...")
    tentativas = 0
    max_tentativas = 5

    while tentativas < max_tentativas:
        try:
            r = requests.get(f"{BASE_URL}/", timeout=3)
            if r.status_code == 200:
                print(f"  API respondeu com sucesso! Status: {r.status_code}")
                print(f"  Resposta: {r.json()}")
                return True
        except requests.ConnectionError:
            tentativas += 1
            print(f"  Tentativa {tentativas}/{max_tentativas} - API nao respondeu, aguardando 2s...")
            time.sleep(2)

    print("\n  [ERRO] API nao esta acessivel em http://localhost:5000")
    print("  Certifique-se de que o Docker esta rodando:")
    print("  -> docker-compose up --build")
    return False


# ========================================================================
# TESTE 1: HEALTH CHECK (GET /)
# ========================================================================
def teste_health_check():
    separador("TESTE 1: HEALTH CHECK - GET /")

    r = requests.get(f"{BASE_URL}/")
    dados = r.json()

    passou = r.status_code == 200 and "mensagem" in dados
    registrar_resultado(
        "GET / -> Health Check",
        passou,
        f"Status: {r.status_code} | Body: {dados}"
    )
    return passou


# ========================================================================
# TESTE 2: CRIAR VAGAS (POST /vagas)
# ========================================================================
def teste_criar_vaga_completa():
    separador("TESTE 2: CRIAR VAGAS - POST /vagas")

    # 2.1 - Criar vaga com campos obrigatorios apenas
    log("2.1 - Criando vaga com campos obrigatorios (empresa + cargo)...")
    payload = {
        "empresa": "Google Brasil",
        "cargo": "Desenvolvedor Junior Python"
    }
    r = requests.post(f"{BASE_URL}/vagas", json=payload)
    dados = r.json()

    passou = r.status_code == 201 and "id" in dados
    if passou:
        ids_criados.append(dados["id"])
    registrar_resultado(
        "POST /vagas -> Criar com campos obrigatorios",
        passou,
        f"Status: {r.status_code} | ID criado: {dados.get('id', 'N/A')} | Resposta: {dados}"
    )

    separador()

    # 2.2 - Criar vaga com TODOS os campos
    log("2.2 - Criando vaga com TODOS os campos preenchidos...")
    payload = {
        "empresa": "Microsoft",
        "cargo": "Backend Engineer",
        "status": "Entrevista Agendada",
        "data_aplicacao": "2026-04-20"
    }
    r = requests.post(f"{BASE_URL}/vagas", json=payload)
    dados = r.json()

    passou = r.status_code == 201 and "id" in dados
    if passou:
        ids_criados.append(dados["id"])
    registrar_resultado(
        "POST /vagas -> Criar com todos os campos",
        passou,
        f"Status: {r.status_code} | ID criado: {dados.get('id', 'N/A')} | Resposta: {dados}"
    )

    separador()

    # 2.3 - Criar mais uma vaga para ter volume de dados
    log("2.3 - Criando terceira vaga para volume de dados...")
    payload = {
        "empresa": "Nubank",
        "cargo": "Analista de Dados",
        "status": "Enviado"
    }
    r = requests.post(f"{BASE_URL}/vagas", json=payload)
    dados = r.json()

    passou = r.status_code == 201 and "id" in dados
    if passou:
        ids_criados.append(dados["id"])
    registrar_resultado(
        "POST /vagas -> Criar terceira vaga",
        passou,
        f"Status: {r.status_code} | ID criado: {dados.get('id', 'N/A')} | Resposta: {dados}"
    )

    separador()

    # 2.4 - Tentar criar vaga SEM empresa (deve dar erro 400)
    log("2.4 - Tentando criar vaga SEM o campo 'empresa' (esperado: erro 400)...")
    payload = {"cargo": "Dev"}
    r = requests.post(f"{BASE_URL}/vagas", json=payload)
    dados = r.json()

    passou = r.status_code == 400 and "erro" in dados
    registrar_resultado(
        "POST /vagas -> Erro 400 (faltando empresa)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    separador()

    # 2.5 - Tentar criar vaga SEM cargo (deve dar erro 400)
    log("2.5 - Tentando criar vaga SEM o campo 'cargo' (esperado: erro 400)...")
    payload = {"empresa": "Amazon"}
    r = requests.post(f"{BASE_URL}/vagas", json=payload)
    dados = r.json()

    passou = r.status_code == 400 and "erro" in dados
    registrar_resultado(
        "POST /vagas -> Erro 400 (faltando cargo)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    separador()

    # 2.6 - Tentar criar vaga com body vazio (deve dar erro 400)
    log("2.6 - Tentando criar vaga com body VAZIO (esperado: erro 400)...")
    r = requests.post(f"{BASE_URL}/vagas", json={})
    dados = r.json()

    passou = r.status_code == 400 and "erro" in dados
    registrar_resultado(
        "POST /vagas -> Erro 400 (body vazio)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )


# ========================================================================
# TESTE 3: LISTAR TODAS AS VAGAS (GET /vagas)
# ========================================================================
def teste_listar_vagas():
    separador("TESTE 3: LISTAR VAGAS - GET /vagas")

    log("Buscando todas as vagas cadastradas no banco...")
    r = requests.get(f"{BASE_URL}/vagas")
    dados = r.json()

    passou = r.status_code == 200 and isinstance(dados, list) and len(dados) >= 3
    registrar_resultado(
        "GET /vagas -> Listar todas",
        passou,
        f"Status: {r.status_code} | Total de vagas retornadas: {len(dados)}"
    )

    # Mostra cada vaga retornada
    log("")
    log("Vagas encontradas no banco:")
    for vaga in dados:
        log(f"  ID: {vaga['id']} | {vaga['empresa']} - {vaga['cargo']} | Status: {vaga['status']} | Data: {vaga.get('data_aplicacao', 'N/A')}")


# ========================================================================
# TESTE 4: BUSCAR VAGA POR ID (GET /vagas/<id>)
# ========================================================================
def teste_buscar_vaga_por_id():
    separador("TESTE 4: BUSCAR VAGA POR ID - GET /vagas/<id>")

    if not ids_criados:
        log("[PULAR] Nenhuma vaga foi criada para buscar.")
        return

    vaga_id = ids_criados[0]

    # 4.1 - Buscar vaga que existe
    log(f"4.1 - Buscando vaga com ID {vaga_id} (deve existir)...")
    r = requests.get(f"{BASE_URL}/vagas/{vaga_id}")
    dados = r.json()

    passou = r.status_code == 200 and dados["id"] == vaga_id
    registrar_resultado(
        f"GET /vagas/{vaga_id} -> Buscar vaga existente",
        passou,
        f"Status: {r.status_code} | Vaga: {dados.get('empresa', 'N/A')} - {dados.get('cargo', 'N/A')}"
    )

    separador()

    # 4.2 - Buscar vaga com ID que NAO existe
    id_inexistente = 99999
    log(f"4.2 - Buscando vaga com ID {id_inexistente} (NAO deve existir, esperado: 404)...")
    r = requests.get(f"{BASE_URL}/vagas/{id_inexistente}")
    dados = r.json()

    passou = r.status_code == 404 and "erro" in dados
    registrar_resultado(
        f"GET /vagas/{id_inexistente} -> Erro 404 (vaga inexistente)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )


# ========================================================================
# TESTE 5: ATUALIZAR VAGA (PUT /vagas/<id>)
# ========================================================================
def teste_atualizar_vaga():
    separador("TESTE 5: ATUALIZAR VAGA - PUT /vagas/<id>")

    if not ids_criados:
        log("[PULAR] Nenhuma vaga foi criada para atualizar.")
        return

    vaga_id = ids_criados[0]

    # 5.1 - Atualizar status da vaga
    log(f"5.1 - Atualizando status da vaga ID {vaga_id} para 'Entrevista Marcada'...")
    payload = {"status": "Entrevista Marcada"}
    r = requests.put(f"{BASE_URL}/vagas/{vaga_id}", json=payload)
    dados = r.json()

    passou = r.status_code == 200 and "mensagem" in dados
    registrar_resultado(
        f"PUT /vagas/{vaga_id} -> Atualizar status",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    separador()

    # 5.2 - Confirmar que a atualizacao foi salva no banco
    log(f"5.2 - Verificando se a atualizacao foi salva no banco (GET /vagas/{vaga_id})...")
    r = requests.get(f"{BASE_URL}/vagas/{vaga_id}")
    dados = r.json()

    passou = r.status_code == 200 and dados.get("status") == "Entrevista Marcada"
    registrar_resultado(
        f"GET /vagas/{vaga_id} -> Confirmar atualizacao no banco",
        passou,
        f"Status atual no banco: '{dados.get('status', 'N/A')}' (esperado: 'Entrevista Marcada')"
    )

    separador()

    # 5.3 - Atualizar empresa e cargo ao mesmo tempo
    log(f"5.3 - Atualizando empresa e cargo da vaga ID {vaga_id}...")
    payload = {
        "empresa": "Google (Atualizado)",
        "cargo": "Senior Developer"
    }
    r = requests.put(f"{BASE_URL}/vagas/{vaga_id}", json=payload)
    dados = r.json()

    passou = r.status_code == 200
    registrar_resultado(
        f"PUT /vagas/{vaga_id} -> Atualizar empresa + cargo",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    # Confirma
    r2 = requests.get(f"{BASE_URL}/vagas/{vaga_id}")
    dados2 = r2.json()
    log(f"         Dados apos update: {dados2.get('empresa')} - {dados2.get('cargo')} - {dados2.get('status')}")

    separador()

    # 5.4 - Tentar atualizar vaga INEXISTENTE (esperado: 404)
    id_inexistente = 99999
    log(f"5.4 - Tentando atualizar vaga inexistente ID {id_inexistente} (esperado: 404)...")
    payload = {"status": "Recusado"}
    r = requests.put(f"{BASE_URL}/vagas/{id_inexistente}", json=payload)
    dados = r.json()

    passou = r.status_code == 404 and "erro" in dados
    registrar_resultado(
        f"PUT /vagas/{id_inexistente} -> Erro 404 (vaga inexistente)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    separador()

    # 5.5 - Tentar atualizar com body vazio (esperado: 400)
    log(f"5.5 - Tentando atualizar vaga ID {vaga_id} com body VAZIO (esperado: 400)...")
    r = requests.put(f"{BASE_URL}/vagas/{vaga_id}", json={})
    dados = r.json()

    passou = r.status_code == 400 and "erro" in dados
    registrar_resultado(
        f"PUT /vagas/{vaga_id} -> Erro 400 (body vazio)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )


# ========================================================================
# TESTE 6: DELETAR VAGAS (DELETE /vagas/<id>)
# ========================================================================
def teste_deletar_vagas():
    separador("TESTE 6: DELETAR VAGAS - DELETE /vagas/<id>")

    if not ids_criados:
        log("[PULAR] Nenhuma vaga foi criada para deletar.")
        return

    # 6.1 - Deletar cada vaga criada durante os testes
    for i, vaga_id in enumerate(ids_criados):
        log(f"6.{i+1} - Deletando vaga ID {vaga_id}...")
        r = requests.delete(f"{BASE_URL}/vagas/{vaga_id}")
        dados = r.json()

        passou = r.status_code == 200 and "mensagem" in dados
        registrar_resultado(
            f"DELETE /vagas/{vaga_id} -> Deletar vaga",
            passou,
            f"Status: {r.status_code} | Resposta: {dados}"
        )

    separador()

    # 6.2 - Tentar deletar novamente (ja foi removida, esperado: 404)
    vaga_id = ids_criados[0]
    log(f"6.{len(ids_criados)+1} - Tentando deletar vaga ID {vaga_id} novamente (esperado: 404)...")
    r = requests.delete(f"{BASE_URL}/vagas/{vaga_id}")
    dados = r.json()

    passou = r.status_code == 404 and "erro" in dados
    registrar_resultado(
        f"DELETE /vagas/{vaga_id} -> Erro 404 (ja foi deletada)",
        passou,
        f"Status: {r.status_code} | Resposta: {dados}"
    )

    separador()

    # 6.3 - Confirmar que o banco ficou limpo (as vagas criadas sumiram)
    log("6.Final - Verificando se as vagas dos testes foram removidas do banco...")
    r = requests.get(f"{BASE_URL}/vagas")
    dados = r.json()

    # Verifica se nenhum ID criado por nos ainda existe
    ids_restantes = [v["id"] for v in dados if v["id"] in ids_criados]
    passou = len(ids_restantes) == 0
    registrar_resultado(
        "GET /vagas -> Confirmar limpeza do banco",
        passou,
        f"IDs de teste restantes no banco: {ids_restantes if ids_restantes else 'Nenhum (limpo!)'}"
    )


# ========================================================================
# EXECUCAO PRINCIPAL
# ========================================================================
if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("  TESTE DE INTEGRACAO REAL - API GERENCIADOR DE VAGAS")
    print("=" * 65)
    print(f"  Alvo: {BASE_URL}")
    print(f"  Data: {date.today().strftime('%d/%m/%Y')}")
    print("=" * 65)

    # Verifica conexao com a API
    if not verificar_api_online():
        sys.exit(1)

    # Executa os testes na ordem logica (CRUD)
    teste_health_check()
    teste_criar_vaga_completa()
    teste_listar_vagas()
    teste_buscar_vaga_por_id()
    teste_atualizar_vaga()
    teste_deletar_vagas()

    # Relatorio final
    print("\n" + "=" * 65)
    print("  RELATORIO FINAL")
    print("=" * 65)
    print(f"  Total de testes executados: {total_testes}")
    print(f"  Aprovados:  {testes_ok}")
    print(f"  Reprovados: {testes_falha}")
    print(f"  Taxa de sucesso: {(testes_ok/total_testes*100):.1f}%")
    print("=" * 65)

    if testes_falha == 0:
        print("\n  RESULTADO: TODOS OS TESTES PASSARAM!")
    else:
        print(f"\n  RESULTADO: {testes_falha} TESTE(S) FALHARAM!")

    print("=" * 65 + "\n")

    # Sai com codigo de erro se algum teste falhou
    sys.exit(0 if testes_falha == 0 else 1)
