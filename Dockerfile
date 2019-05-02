FROM python:3

WORKDIR /var/www

COPY ./nginx.list /etc/apt/sources.list.d/
COPY ./nginx_signing.key /var/www/
RUN apt-key add nginx_signing.key && \
    apt -y update && \
    apt -y install nginx
COPY ./default.conf /etc/nginx/conf.d/
COPY ./.htpasswd /etc/nginx/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./supervisord.conf /etc/supervisord.conf

RUN rm -rf /var/www/app/tmp
RUN mkdir -p /var/www/app/tmp
COPY ./app /var/www/app
COPY ./startup.sh /var/www/startup.sh
COPY ./startup_local.sh /var/www/startup_local.sh
RUN chmod 755 /var/www/startup.sh

CMD [ "/var/www/startup.sh" ]
