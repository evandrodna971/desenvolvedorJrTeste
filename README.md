# Gerenciador de Vagas de Emprego 🚀

Esse aqui é um projeto de API backend pra gerenciar vagas de emprego aplicadas. Sabe quando a gente manda vários currículos e perde o controle de onde mandou e o que rolou depois? Essa API veio pra ajudar a registrar essas vagas e o status (se foi chamado pra entrevista, se está em análise, se foi recusado etc).

Escolhi essa ideia pra fugir um pouco do clássico "To-Do List" ou "Gerenciador de Contatos" e mostrar um pouquinho além do básico. Pensei numa ferramenta que eu realmente utilizaria no meu dia a dia de busca por vagas.

## 🛠 Tecnologias que utilizei

- **Python:** Escolhi Python pq acho super limpo, direto e eu consigo focar 100% em construir a lógica.
- **Flask:** Um micro-framework leve, bom que não tem muita "magia" por trás dele fazendo o trabalho sozinho. Isso me permite mostrar que sei montar do zero as rotas HTTP e receber as requisições direitinho.
- **PostgreSQL:** Banco de dados relacional super robusto. Utilizei as consultas de `.sql` raiz diretamente no código através do pacote `psycopg2`. Deixei de fora ORMs (como o SQLAlchemy) pra deixar bem claro meu conhecimento nos comandos SQL em si.
- **Docker e Docker Compose (Diferencial):** Pra não ter aquelas dores de cabeça do tipo "na minha máquina funciona, mas aqui quebrou", joguei tudo num container. É só dar um comando e o próprio Docker levanta o banco de dados e a API juntos conversando entre si.

## ⚙️ Como Instalar e Rodar na sua Máquina

### Opção 1: Usando Docker (Recomendado e mais fácil)
Você só precisa ter o Docker e o Docker Compose instalados no seu PC.
1. Baixe os arquivos do projeto (clona ai do git).
2. Abra o terminal na pasta principal e roda o comando:
   ```bash
   docker-compose up --build
   ```
3. Aguarde uns segundinhos para os containers subirem. Pronto! A API já vai estar rodando na sua máquina apontando pra porta `5000`.

### Opção 2: Rodando Localmente (Sem o Docker)
Caso você já tenha o banco de dados PostgreSQL rodando cru na sua máquina:
1. Tenha o Python rodando de boa na sua máquina.
2. Crie e ative um ambiente virtual (não é obrigatório mas sempre recomendo pra n sujar a máquina toda):
   ```bash
   python -m venv venv
   # no windows:
   venv\Scripts\activate
   # no linux:
   source venv/bin/activate
   ```
3. Instala aí as dependências que listei no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Cria um banco de dados em branco chamado `vagas_db` no seu PostgreSQL.
5. Eu não criei o `.env` aqui do local pra API não dar B.O pra vocês testarem. Assim ela puxa no `app.py` um link padrão tipo `postgresql://dev_user:dev_password@localhost:5432/vagas_db`. Troca as credenciais lá caso precise!
6. Roda o programa!
   ```bash
   python src/app.py
   ```

**Dica:** A tabela do banco (`vagas`) é gerada automaticamente pelo Python na primeira vez que a aplicação levanta! Facilita né?

## 📚 Como testar a API?
Depois de botar o programa pra rodar (em `http://localhost:5000`), você usa qualquer client como Postman, Insomnia ou até o cURL no prompt de comando.

Mas olha, fiz uma documentação bem mastigada aqui também. Tem um arquivo chamado `DOCUMENTACAO.md` e está salvo na mesma pasta! Eu detalhei cada uma das rotas e os dados que tem que enviar de forma bem simplificada pra facilitar.
