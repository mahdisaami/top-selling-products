FROM python:alpine

LABEL maintainer="Mahdi <mahdisaami7828@gmail.com>"

WORKDIR /best_selling

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    build-base

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
