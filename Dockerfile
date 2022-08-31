FROM python:latest

RUN apt update && apt install jenkins-job-builder -y 1>/dev/null 2>&1

RUN mkdir /cockpit
RUN mkdir /config
RUN mkdir /manifest
RUN mkdir /grafana_dashboard

WORKDIR /cockpit/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./cockpit/ ./
COPY ./manifest/ /manifest/
COPY ./grafana_dashboard/ /grafana_dashboard/

ENV "JENKINS_CONFIG"="/config"
ENV "MANIFEST_PATH"="/manifest"

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]