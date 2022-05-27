FROM python:latest

RUN apt install jenkins-job-builder -y 1> /dev/null 2>&1

RUN mkdir /cockpit
RUN mkdir /config

WORKDIR /cockpit/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./cockpit/ ./

ENV "JENKINS_CONFIG"="/config"

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]