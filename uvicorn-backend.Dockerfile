# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR .
ENV FLASK_APP=webex-skill.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers build-base openldap-dev python3-dev
#last argument of copy is destination
COPY ["webex-skill.py", \
    "requirements.txt", \
    "./"]
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "webex-skill.py"]