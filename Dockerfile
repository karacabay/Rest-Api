FROM python:3.7-buster
WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update

COPY . .
