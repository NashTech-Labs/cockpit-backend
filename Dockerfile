FROM python:latest

RUN mkdir /cockpit

WORKDIR /cockpit/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./cockpit/ ./

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]