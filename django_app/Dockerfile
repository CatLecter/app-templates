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

CMD uwsgi --http-socket 0.0.0.0:8000 \
    --plugin=python \
    --wsgi-file ./config/wsgi.py \
    --callable application \
    --master \
    --workers=3 \
    --disable-logging \
    --log-4xx \
    --log-5xx
