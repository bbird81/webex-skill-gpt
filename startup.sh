#!/bin/sh
echo "***********SKILL SECRECTS**********"
cat /lutech/.env
echo "***********************************"
echo "---------> PUBLIC KEY <------------"
cat /lutech/cat id_rsa.pub
webex-skills skills run lutech