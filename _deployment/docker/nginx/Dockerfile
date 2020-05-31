FROM nginx:1.17.1

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./_deployment/docker/nginx/sources.list /etc/apt/

#RUN apt-get update
#RUN apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./_deployment/docker/nginx/dyezweb.conf /etc/nginx/conf.d/dyezweb.conf