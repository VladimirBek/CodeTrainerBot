FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

