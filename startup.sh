#!/bin/sh
if [ -z $OPENAI_KEY]; # if string is empty
then
    echo "OpenAI API token not set: ABORTING!"
else
    echo "***********SKILL SECRECTS**********"
    cat /wbxskill/.env
    echo
    echo "***********************************"
    echo "---------> PUBLIC KEY <------------"
    cat /wbxskill/id_rsa.pub
    echo "Token OpenAI: $OPENAI_KEY"
    cd /wbxskill
    uvicorn --port 8080 --host 0.0.0.0 --reload wbxskill.main:api
fi