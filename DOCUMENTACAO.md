# Documentação da API - Gerenciador de Vagas

Essa documentação serve para você entender cada endpoint da nossa API de Vagas!
A URL base local será sempre: `http://localhost:5000`

---

## 1. Rota Principal
Serve como um "Health Check". Basicamente vê se a API subiu sem dar pau.

- **URL:** `/`
- **Método HTTP:** `GET`
- **Request Body:** Não envia nada.
- **Response (200 OK):**
  ```json
  {
    "mensagem": "API de Vagas rodando tranquilamente!"
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
  - `data_aplicacao` (Opcional, Data YYYY-MM-DD) -> Se ignorar, ele chuta pro bd usar a data de atual do dia.
  
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
    "erro": "Vish, esqueceu algo! 'empresa' e 'cargo' são campos obrigatórios."
  }
  ```

---

## 3. Listar Todas as Vagas
Baixa a lista de geral que você salvou antes.

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
Aquele famoso UPDATE. Útil quando você tava no status "Enviado", e a empresa mandou email marcando entrevista. Ai você vai lá e avisa atualiza o status dela.

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
    "mensagem": "Informações atualizadas certinho!"
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
Sumiu com todas as esperanças da vaga ou duplicou na hora de salvar? Usa o DELETAR pra extirpar do banco de dados (o banco que perdoe).

- **URL:** `/vagas/<id>`
- **Método HTTP:** `DELETE`
- **Request Body:** Nada denovo.
- **Response Sucesso (200 OK):**
  ```json
  {
    "mensagem": "Vaga apagada do histórico."
  }
  ```
- **Response Erro (404 Not Found):**
  ```json
  {
    "erro": "Vaga não encontrada pra deletar."
  }
  ```

---

## Padrões de Códigos de Erro (Http Status Code)
Só de bate pronto, pra você não se perder:
- `200` (OK): Tudo que eu te mandei você me entregou ou eu processei tranquilamente.
- `201` (Created): Você cadastrou e eu salvei!
- `400` (Bad Request): Foi mandado algum formato errado pra mim, tipo faltar um dado exigido.
- `404` (Not Found): Aquele id especificado simplesmente não acha nada.
- `500` (Internal Server Error): Deu panico. Erro feio geralmente de banco fora do ar ou eu digitei o SQL errado. Eu deixei um block `try/except` segurando tudo, para ele devolver como erro limpo no final para mim e não quebrar subitamente o terminal em si.
