FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

# 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk update \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  && apk add gcc musl-dev git

WORKDIR /projects

RUN git clone https://gitee.com/zjdyez/dyezweb.git

# 配置文件里面有不能外泄的密钥，所以没有提交到 gitee 上，只能本地拷贝！
COPY ./_deployment/docker/local/django/settings.py  dyezweb/dyezweb/

RUN pip install -r /projects/dyezweb/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

RUN pip install -r /projects/dyezweb/_deployment/docker/local/django/requirements_extra.txt -i https://mirrors.aliyun.com/pypi/simple


RUN sed -i 's/\r//' /projects/dyezweb/_deployment/docker/local/django/start.sh

RUN chmod +x /projects/dyezweb/_deployment/docker/local/django/start.sh