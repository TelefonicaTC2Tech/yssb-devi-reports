FROM python:3.10.4-slim-buster

RUN apt-get update && \
    apt-get install -y build-essential libpango1.0-0

COPY requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /src
