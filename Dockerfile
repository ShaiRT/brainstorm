FROM python:3.8-slim-buster

RUN apt-get update -y
RUN apt-get install -y npm
RUN npm install -g npm@latest

ADD requirements.txt /requirements.txt
RUN pip3.8 install -r requirements.txt

ADD scripts/wait-for-it.sh /wait-for-it.sh

ADD brainstorm /brainstorm
RUN npm install /brainstorm/gui/gui-app

EXPOSE 8000 5000 8080