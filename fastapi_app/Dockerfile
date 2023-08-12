FROM python:3.11.4-bookworm

EXPOSE 8000

WORKDIR /usr/src/app

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app --log-level warning
