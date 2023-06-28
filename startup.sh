#!/bin/sh
if [$OPENAI_KEY];
then
    echo "***********SKILL SECRECTS**********"
    cat /wbxskill/.env
    echo
    echo "***********************************"
    echo "---------> PUBLIC KEY <------------"
    cat /wbxskill/id_rsa.pub
    echo "Token OpenAI: $OPENAI_KEY"
    cd /wbxskill
    uvicorn --port 8080 --host 0.0.0.0 --reload wbxskill.main:api
else
    echo "OpenAI API token not set: ABORTING!"
fi