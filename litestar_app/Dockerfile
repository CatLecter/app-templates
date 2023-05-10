FROM python:3.11.3-bullseye

EXPOSE 5000

WORKDIR /usr/src/app

RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port 5000 --workers 1
