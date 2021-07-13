FROM ubuntu:18.04

LABEL maintainer="Jose Eduardo Casillas <jose.e.casillas@gmail.com>"
LABEL description="Currency Exchange Challenge App project"
LABEL version="0.1"

WORKDIR /challengeapp

COPY . /challengeapp

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install flask==2.0.1

EXPOSE 7700

CMD ["python3","currencyExchange_webhook.py","--debug","1"]
