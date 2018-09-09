FROM python:alpine

RUN mkdir /app

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV="docker"
ENV FLASK_APP="app.py"

EXPOSE 5000
