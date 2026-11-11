# syntax=docker/dockerfile:1
FROM python:3.11-alpine

LABEL maintainer="https://github.com/King-Greatman-Spirit"

ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

# Create the virtual environment
RUN python3 -m venv /opt/venv

# Install dependencies and upgrade pip
RUN apk add --no-cache zlib-dev jpeg-dev gcc musl-dev && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --upgrade -r requirements.txt && \
    chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
