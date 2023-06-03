# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /
ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers build-base openldap-dev python3-dev
RUN apk add --no-cache gcc musl-dev linux-headers build-base
#last argument of copy is destination
COPY ["webex-skill.py", \
    "requirements.txt", \
    "startup.sh", \
    "tokens.py", \
    "./"]
RUN pip install -r requirements.txt
RUN webex-skills project init lutech
RUN mv /webex-skill.py /lutech/lutech/main.py && mv /tokens.py /lutech/lutech/
RUN chmod +x ./startup.sh
#RUN echo "***********SKILL SECRECTS**********\n" && cat /lutech/.env
EXPOSE 8080
CMD ["/bin/sh", "-c", "./startup.sh"]
#CMD ["webex-skills", "webex-skill.py"]