FROM python:3.9-alpine

# Instalar Docker CLI e dependências necessárias
RUN apk --no-cache add \
    docker \
    bash \
    gcc \
    libc-dev \
    libffi-dev \
    openssl-dev

# Instalar dependências do Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código para o diretório de trabalho
COPY ./app /app
WORKDIR /app

ENTRYPOINT ["python", "deploy.py"]
