# Documentação da API - Gerenciador de Vagas

Essa documentação serve para você entender cada endpoint da nossa API de Vagas!
A URL base local será sempre: `http://localhost:5000`

---

## 1. Rota Principal
Serve como um "Health Check". Basicamente vê se a API subiu sem dar problema.

- **URL:** `/`
- **Método HTTP:** `GET`
- **Request Body:** Não envia nada.
- **Response (200 OK):**
  ```json
  {
    "mensagem": "API de Vagas Ativa!"
  }
  ```

---

## 2. Criar uma nova Vaga
Cria um registro novo no banco de uma vaga de emprego ou envio de currículo que você fez.

- **URL:** `/vagas`
- **Método HTTP:** `POST`
- **Request Body (JSON):**
  - `empresa` (Obrigatório, String)
  - `cargo` (Obrigatório, String)
  - `status` (Opcional, String) -> Se não pôr, ele salva "Enviado" por padrão.
  - `data_aplicacao` (Opcional, Data YYYY-MM-DD) -> Se ignorar, ele salva a data atual do dia.
  
  Exemplo do que seria enviado no seu Insomnia:
  ```json
  {
    "empresa": "NuBank",
    "cargo": "Desenvolvedor Backend Jr",
    "status": "Enviado"
  }
  ```
- **Response Sucesso (201 Created):**
  ```json
  {
    "id": 1,
    "mensagem": "Vaga registrada na base com sucesso!"
  }
  ```
- **Response Erro - Usuário esqueceu mandou incompleto (400 Bad Request):**
  ```json
  {
    "erro": "Esqueceu algo! 'empresa' e 'cargo' são campos obrigatórios."
  }
  ```

---

## 3. Listar Todas as Vagas
Baixa a lista geral que você salvou.

- **URL:** `/vagas`
- **Método HTTP:** `GET`
- **Request Body:** Vazio
- **Response Sucesso (200 OK):**
  ```json
  [
    {
      "id": 2,
      "empresa": "Ifood",
      "cargo": "Engenheiro de Software",
      "status": "Entrevista Técnica",
      "data_aplicacao": "Tue, 15 Apr 2025 00:00:00 GMT"
    },
    {
      "id": 1,
      "empresa": "NuBank",
      "cargo": "Desenvolvedor Backend Jr",
      "status": "Enviado",
      "data_aplicacao": "Thu, 17 Apr 2025 00:00:00 GMT"
    }
  ]
  ```

---

## 4. Buscar Uma Vaga pelo ID
Traz so uma vaga passando o `ID` lá no final da Rota de chamada.

- **URL:** `/vagas/<id>`  (Exemplo de uso: `/vagas/1`)
- **Método HTTP:** `GET`
- **Request Body:** Nenhum.
- **Response Sucesso (200 OK):**
  ```json
  {
    "id": 1,
    "empresa": "NuBank",
    "cargo": "Desenvolvedor Backend Jr",
    "status": "Enviado",
    "data_aplicacao": "Thu, 17 Apr 2025 00:00:00 GMT"
  }
  ```
- **Response Erro - Não encontrou a Vaga (404 Not Found):**
  ```json
  {
    "erro": "Vaga não encontrada no sistema"
  }
  ```

---

## 5. Atualizar Vaga
Aquele famoso UPDATE. Útil quando você estava no status "Enviado", e a empresa mandou email marcando entrevista. Ai você vai lá e avisa atualiza o status dela.

- **URL:** `/vagas/<id>` (Exemplo: `/vagas/1`)
- **Método HTTP:** `PUT`
- **Request Body (Passa só aquilo que quiser mudar!):**
  ```json
  {
    "status": "Aprovado!!"
  }
  ```
- **Response Sucesso (200 OK):**
  ```json
  {
    "mensagem": "Informações atualizadas!"
  }
  ```
- **Response Erro (404 Not Found):**
  ```json
  {
    "erro": "Vaga não encontrada"
  }
  ```

---

## 6. Deletar Vaga
Sumiu com todas as esperanças da vaga ou duplicou na hora de salvar? Usa o DELETAR pra apagar do banco de dados.

- **URL:** `/vagas/<id>`
- **Método HTTP:** `DELETE`
- **Request Body:** Nada.
- **Response Sucesso (200 OK):**
  ```json
  {
    "mensagem": "Vaga apagada."
  }
  ```
- **Response Erro (404 Not Found):**
  ```json
  {
    "erro": "Vaga não encontrada."
  }
  ```

---

## Padrões de Códigos de Erro (Http Status Code)
Para você não se perder:
- `200` (OK): Tudo que eu te mandei você me entregou ou eu processei.
- `201` (Created): Você cadastrou e eu salvei!
- `400` (Bad Request): Foi mandado algum formato errado para mim, tipo faltar um dado exigido.
- `404` (Not Found): Aquele id especificado simplesmente não acha nada.
- `500` (Internal Server Error): Erro feio geralmente de banco fora do ar ou eu digitei o SQL errado. Eu deixei um block `try/except` segurando tudo, para ele devolver como erro limpo no final para mim e não quebrar subitamente o terminal em si.

---

## 📋 EXEMPLOS NO POWERSHELL PARA VOCÊ TESTAR A API

## 1. 📝 POST - Criar vaga (todos os campos)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas" -Method POST -ContentType "application/json" -Body '{"empresa":"Microsoft","cargo":"Backend Engineer","status":"Entrevista Agendada","data_aplicacao":"2026-04-20"}'
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 2. 📝 POST - Criar vaga (só obrigatórios)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas" -Method POST -ContentType "application/json" -Body '{"empresa":"Google Brasil","cargo":"Desenvolvedor Junior Python"}'
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 3. 📋 GET - Listar todas as vagas

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas" -Method GET
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 4. 🔍 GET - Buscar vaga por ID (substitua 1 pelo ID)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas/1" -Method GET
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 5. ✏️ PUT - Atualizar vaga inteira (substitua 1 pelo ID)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas/1" -Method PUT -ContentType "application/json" -Body '{"empresa":"Amazon","cargo":"Senior Python","status":"Aprovado","data_aplicacao":"2026-04-21"}'
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 6. 🔧 PATCH - Atualizar campo específico (substitua 1 pelo ID)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas/1" -Method PATCH -ContentType "application/json" -Body '{"status":"Entrevista Final"}'
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

## 7. ❌ DELETE - Deletar vaga (substitua 1 pelo ID)

$r = Invoke-WebRequest -Uri "http://localhost:5000/vagas/1" -Method DELETE
;Write-Host "Status:" $r.StatusCode
;Write-Host "Resposta:" $r.Content

---

## 🧪 Testes Automatizados da API

Foi criado um script robusto na pasta `/tests` (`test_rotas.py`). Ele fará todo o fluxo completo em questão de milissegundos testando diretamente no banco em ambiente Docker:

1. Subirá 3 vagas completas reais no banco (para testar os `201 Created`);
2. Forçará vagas nulas e vazias (para acionar os `400 BadRequest`);
3. Buscará uma lista enorme com essas vagas e filtrará uma pela ID;
4. Digitará e tentará buscar uma ID absurda e inexistente pra forçar os `404 Not Found`;
5. Fará updates e depois confirmará sozinho via GET pra averiguar se o salvamento foi concluído;
6. Limpará todo o banco deletando cada ID criada (sem mexer naquelas que você mesmo cadastrou).

**Como acionar a verificação:**
Com os containers Docker rodando as instâncias normais do projeto, digite no terminal principal:
`python tests/test_rotas.py`
