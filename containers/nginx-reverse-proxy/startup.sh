#!/bin/sh
if [ -z $FQDN ]; # if FQDN env var is empty
then
    echo "FQDN env var not set: ABORTING!"
else
    echo "***************** FQDN *****************"
    echo " Your server fqdn is $FQDN"
    echo "****************************************"
    sed -i "s/your_server_fqdn/$FQDN/" /etc/nginx/conf.d/default.conf
    echo default.conf file:
    echo "------------------------------------------------------"
    cat /etc/nginx/conf.d/default.conf
    echo "------------------------------------------------------"
    echo "Starting NGINX..."
    nginx -g 'daemon off;'
fi