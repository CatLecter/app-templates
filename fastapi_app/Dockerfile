FROM python:3.11.5-bookworm as base

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

FROM base

EXPOSE 8000

WORKDIR /usr/src/app

COPY . .

RUN poetry install

CMD gunicorn main:app \
    --workers 3 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --log-level warning
