FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

# 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  && apk add gcc musl-dev

WORKDIR /app

#当然有些文件对于程序运行是不必要的，
# .dockerignore 文件里面指定的文件不会被 copy 到容器里。
COPY . /app

COPY ._deployment/docker/local/django/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY ._deployment/docker/local/django/start.sh /start.sh

RUN sed -i 's/\r//' /start.sh

RUN chmod +x /start.sh