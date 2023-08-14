FROM python:3.7-buster
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install requests
RUN apt-get update

COPY . .
