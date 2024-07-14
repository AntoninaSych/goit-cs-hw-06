# Dockerfile для HTTP-сервера та Socket-сервера
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 3000 5001

CMD ["python", "main.py"]
