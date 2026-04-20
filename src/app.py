import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

# Pega a URL do banco das variaveis de ambiente caso encontre (como passamos do docker-compose)
# Se não achar nada (tipo num teste rodando seco no Python localmente), vai bater nessa string ali 
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://dev_user:dev_password@localhost:5432/vagas_db")


def get_db_connection():
    """
    Essa função é responsável por simplesmente abrir as portinhas pro Postgres.
    """
    try:
        # Usa o RealDictCursor pq facilita a minha vida, ao invés de buscar os dados numa lista maluca (1, 'Vaga', etc), 
        # esse pacote já estrutura num dicionário {'id': 1, 'nome': 'Vaga'} para enviar pra API ficar igual ao JSON.
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"B.O na hora de conectar lá banco de dados: {e}")
        return None

def criar_tabela():
    """
    Cria a tabela no banco quando o programa subir
    Achei util fazer isso pra gente não ter que rodar nenhum script SQL externo.
    O código inicia e caso nao exista, a tabela pipoca por conta própria no bd.
    """
    conn = get_db_connection()
    if conn is None:
        print("Atenção: Não conseguiu conectar. Confere se o BD já terminou processo de Start!")
        return
        
    try:
        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS vagas (
            id SERIAL PRIMARY KEY,
            empresa VARCHAR(100) NOT NULL,
            cargo VARCHAR(100) NOT NULL,
            status VARCHAR(50) DEFAULT 'Enviado',
            data_aplicacao DATE DEFAULT CURRENT_DATE
        );
        """
        cursor.execute(query)
        conn.commit() # consolida criação
    except Exception as e:
        print(f"Deu erro ao criar a tabela viu: {e}")
    finally:
        # Importante fechar sempre para não sobrar conexões vazando memoria e travando o postgres
        cursor.close()
        conn.close()

# Chamando lá em cima na largada da máquina
criar_tabela()


@app.route('/', methods=['GET'])
def index():
    # Rota raiz só ver se o server está pendurado vivo
    return jsonify({"mensagem": "API de Vagas rodando tranquilamente!"}), 200

@app.route('/vagas', methods=['POST'])
def criar_vaga():
    # Puxa no Request o json do usuário
    dados = request.get_json()
    
    # Validação pequena ali pra não criar sem nada no banco vazio que é feio
    if not dados or 'empresa' not in dados or 'cargo' not in dados:
        return jsonify({"erro": "Vish, esqueceu algo! 'empresa' e 'cargo' são campos obrigatórios."}), 400
        
    empresa = dados['empresa']
    cargo = dados['cargo']
    status = dados.get('status', 'Enviado') # se nao botar o cara mandou enviou apenas
    data_aplicacao = dados.get('data_aplicacao', None) 
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"erro": "Banco de dados fora do ar."}), 500

    cursor = conn.cursor()
    
    try:
        # Protegendo usando o %s (parametros bindables) pra ninguém jogar "DROP TABLE" la e foder meu sistema (SQL inject)
        if data_aplicacao:
            # O RETURNING id é um bizu massa! Assim eu já gravo e pego de volta que a DB escolheu qual foi ID gerado sem fazer outro SELECT p achar
            comando = "INSERT INTO vagas (empresa, cargo, status, data_aplicacao) VALUES (%s, %s, %s, %s) RETURNING id;"
            cursor.execute(comando, (empresa, cargo, status, data_aplicacao))
        else:
            comando = "INSERT INTO vagas (empresa, cargo, status) VALUES (%s, %s, %s) RETURNING id;"
            cursor.execute(comando, (empresa, cargo, status))
            
        id_inserido = cursor.fetchone()['id']
        conn.commit() # Salva p sempre
        
        return jsonify({
            "mensagem": "Vaga registrada na base com sucesso!",
            "id": id_inserido
        }), 201 
        
    except Exception as e:
        conn.rollback() # Se estourar algum erro no meio de tudo em cima ali, aborta transação do banco 
        return jsonify({"erro": f"Erro interno brabo: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/vagas', methods=['GET'])
def listar_vagas():
    # Lista de geral decrescente pelo id
    conn = get_db_connection()
    if not conn:
        return jsonify({"erro": "Banco de dados fora do ar."}), 500
        
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM vagas ORDER BY id DESC;")
        # fechall puxa os dicio todinhos numa listona (o RealDictCursor formata por mim ali em cima antes)
        vagas = cursor.fetchall() 
        return jsonify(vagas), 200
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/vagas/<int:vaga_id>', methods=['GET'])
def buscar_uma_vaga(vaga_id):
    conn = get_db_connection()
    if not conn:
         return jsonify({"erro": "Banco de dados fora do ar."}), 500

    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM vagas WHERE id = %s;", (vaga_id,))
        vaga = cursor.fetchone()
        
        # Testinho p ver se n pediram coisa de excluso antes
        if not vaga:
            return jsonify({"erro": "Vaga não encontrada no sistema"}), 404
            
        return jsonify(vaga), 200
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/vagas/<int:vaga_id>', methods=['PUT'])
def atualizar_vaga(vaga_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado recebido no body para editar."}), 400
        
    conn = get_db_connection()
    if not conn:
         return jsonify({"erro": "Banco de dados fora do ar."}), 500
    cursor = conn.cursor()
    
    try:
        # Primeiro confere que ela existe, pq n adianta tacar agua no teto.
        cursor.execute("SELECT * FROM vagas WHERE id = %s;", (vaga_id,))
        vaga_existente = cursor.fetchone()
        
        if not vaga_existente:
            return jsonify({"erro": "Vaga não encontrada"}), 404
            
        # Pega as informações dadas agr pela api. SE não vier algo do json, pegamos a "velha" do banco antes
        empresa = dados.get('empresa', vaga_existente['empresa'])
        cargo = dados.get('cargo', vaga_existente['cargo'])
        status = dados.get('status', vaga_existente['status'])
        
        sql = "UPDATE vagas SET empresa = %s, cargo = %s, status = %s WHERE id = %s;"
        cursor.execute(sql, (empresa, cargo, status, vaga_id))
        conn.commit()
        
        return jsonify({"mensagem": "Informações atualizadas certinho!"}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/vagas/<int:vaga_id>', methods=['DELETE'])
def deletar_vaga(vaga_id):
    conn = get_db_connection()
    if not conn:
         return jsonify({"erro": "Banco de dados fora do ar."}), 500
    cursor = conn.cursor()
    
    try:
        # Um RETURNING salvador pra já ter ctz que deleta
        # se nn ter id na resposta eh pq não achou
        cursor.execute("DELETE FROM vagas WHERE id = %s RETURNING id;", (vaga_id,))
        retorno = cursor.fetchone()
        
        if not retorno:
            return jsonify({"erro": "Vaga não encontrada pra deletar."}), 404
            
        conn.commit()
        return jsonify({"mensagem": "Vaga apagada do histórico."}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Roda p cima aqui, colado em qualquer IP assim ele alcança a rededo docker (usando 5000) de boa
    app.run(host='0.0.0.0', port=5000, debug=True)
