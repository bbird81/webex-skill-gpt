#!/bin/sh
echo "***********SKILL SECRECTS**********"
cat /lutech/.env
echo
echo "***********************************"
echo "---------> PUBLIC KEY <------------"
cat /lutech/id_rsa.pub
#webex-skills skills run lutech
cd /lutech
uvicorn --port 8080 --host 0.0.0.0 --reload lutech.main:api