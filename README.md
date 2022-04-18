# cockpit-backend

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