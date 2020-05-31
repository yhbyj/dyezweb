FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev libffi-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
COPY  ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN apk del .tmp-build-deps

# mkdir is not working
RUN mkdir -p /project/{static,media}
WORKDIR /project
COPY  ./ /project

RUN adduser -D user
USER user