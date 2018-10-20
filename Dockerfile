FROM python:alpine

RUN mkdir /app

COPY app/ /app
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk add postgresql-dev
RUN apk add build-base
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV="docker"
ENV FLASK_APP="app.py"

EXPOSE 5000
