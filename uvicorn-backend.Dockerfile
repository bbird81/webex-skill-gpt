# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /
COPY ["webex-skill.py", \
    "requirements.txt", \
    "startup.sh", \
    "./"]
RUN pip install -r requirements.txt
RUN webex-skills project init wbxskill
RUN mv /webex-skill.py /wbxskill/wbxskill/main.py
RUN chmod +x ./startup.sh
EXPOSE 8080
CMD ["/bin/sh", "-c", "./startup.sh"]