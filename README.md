# cockpit-backend
# TechStack
1.Django-Python Framework
2.Python Libs:
    Django==4.0.3
    #guacapy==0.11.0
    psycopg2-binary==2.9.3
    websocket-client==1.3.2
    celery==5.2.3
    simplejson==3.17.6
    requests==2.27.1
    boto3==1.21.43
3.Gucamole
4.Postgres_DB
5.Bash Scripting
6.Liquibase
7.Packer
8.Jenkins
9.AWS Resource:
    a.ec2-instance
    b.IAM
    c.s3
    d.route-53
    e.vpc
    f.sqs
# how to run the Project on non-docker-env

# 0. Clone the source code from github
# 1. create python virtual_env 
    ```
    command : python3 -m venv ./venv
    activation : source ./venv/bin/activate
    ```
# 2. install dependencies
    ```command: pip3 -r install ./requirements.txt```
# 3. run celery worker
    ```command: cd ./cockpit 
    command: celery  -A cockpit worker --loglevel=INFO```
# 4. run django server
    ```command: python3 manage.py runserver 0.0.0.0:8000```
# 5 rabbitmq runs
    ```command : docker run -d -p 5672:5672 rabbitmq```