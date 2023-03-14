#!/bin/sh
echo "***********SKILL SECRECTS**********"
cat /lutech/.env
echo
echo "***********************************"
echo "---------> PUBLIC KEY <------------"
cat /lutech/id_rsa.pub
webex-skills skills run lutech