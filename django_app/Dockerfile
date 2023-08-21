FROM python:3.11.4-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

EXPOSE 8000

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt \
    && python manage.py spectacular --file schema.yml \
    && python manage.py collectstatic --noinput

CMD uwsgi --http-socket 0.0.0.0:8000 \
    --plugin=python \
    --wsgi-file ./config/wsgi.py \
    --callable application \
    --master \
    --workers=3 \
    --disable-logging \
    --log-4xx \
    --log-5xx