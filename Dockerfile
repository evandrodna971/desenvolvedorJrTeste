# Uso uma imagem oficial do Python, a versao slim ocupa pouco espaço
FROM python:3.11-slim

# Crio e entro na pasta app dentro do container
WORKDIR /app

# Copiar os requerimentos antes do código agiliza os builds futuros já que o pip só roda de novo se mudar um pacote
COPY requirements.txt .

# Instalo as dependências sem deixar sujeira no cache
RUN pip install --no-cache-dir -r requirements.txt

# Copio tudo que eu programei para dentro do meu ambiente
COPY . .

# Explicita que a porta 5000 está virada para o mundo externo
EXPOSE 5000

# Executa o app
CMD ["python", "src/app.py"]
