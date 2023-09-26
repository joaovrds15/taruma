# Use a imagem base do Python 3
FROM python:3

# Atualize o sistema de pacotes
RUN apt-get update

# Crie o diretório de trabalho /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt requirements.txt

# Atualize o pip e instale as dependências do Python
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório atual para o diretório de trabalho
COPY . .

EXPOSE 80:8000

# Comando para executar o arquivo manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN python manage.py migrate