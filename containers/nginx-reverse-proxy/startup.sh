#!/bin/sh
echo "*********** FQDN **********"
echo "Your server fqdn is $FQDN"
echo "***************************"
sed -i "s/your_server_fqdn/$FQDN/" /etc/nginx/conf.d/default.conf
echo default.conf file:
cat /etc/nginx/conf.d/default.conf