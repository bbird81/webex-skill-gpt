FROM nginx:latest
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./startup.sh /
COPY ./backend-not-found.html /var/www/html/backend-not-found.html
#includes directory contains proxy.conf and ssl.conf
COPY ./includes/ /etc/nginx/includes/
#ssl directory contains certificates
COPY ./certificates /etc/ssl/certs/nginx/
RUN chmod +x ./startup.sh
CMD ["/bin/sh", "-c", "./startup.sh"]