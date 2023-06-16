#!/bin/sh
echo "***********SKILL SECRECTS**********"
cat /wbxskill/.env
echo
echo "***********************************"
echo "---------> PUBLIC KEY <------------"
cat /wbxskill/id_rsa.pub
echo "Token OpenAI: $OPENAPI_KEY"
cd /wbxskill
uvicorn --port 8080 --host 0.0.0.0 --reload wbxskill.main:api