# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# **NOVO PASSO CRÍTICO:** Copie APENAS o requirements.txt para o diretório de trabalho do container.
# Isso garante que o Docker Builder sempre reavalie esta etapa se o requirements.txt mudar.
COPY requirements.txt ./

# Instale todas as dependências Python listadas em requirements.txt.
# Agora, o pip vai encontrar o arquivo garantidamente.
RUN pip install --no-cache-dir -r ./requirements.txt

# **NOVO PASSO CRÍTICO:** Copie o restante do código da sua aplicação.
# Isso é feito APÓS a instalação das dependências para otimizar o cache,
# pois o código da aplicação muda com mais frequência do que as dependências.
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]