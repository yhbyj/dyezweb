FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

#替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev libffi-dev linux-headers postgresql-dev

RUN mkdir -p /projects/dyezweb

WORKDIR /projects/dyezweb

COPY  ./ /projects/dyezweb

RUN pip install -r /projects/dyezweb/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

RUN apk del .tmp-build-deps

RUN adduser -D user

USER user