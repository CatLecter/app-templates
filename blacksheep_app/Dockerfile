FROM python:3.11.3-bullseye

EXPOSE 8000

WORKDIR /usr/src/app

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001 main:app --log-level warning
