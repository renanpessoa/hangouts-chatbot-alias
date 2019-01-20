FROM python:3-alpine

MAINTAINER Renan Pessoa

WORKDIR /chat_bot

COPY . /chat_bot

RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev \
            tzdata

RUN cp /usr/share/zoneinfo/Brazil/East /etc/localtime

RUN apk add --no-cache pcre

RUN pip install -r requirements.txt

RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

EXPOSE 5000

CMD ["uwsgi", "--ini", "/chat_bot/project.ini"]
