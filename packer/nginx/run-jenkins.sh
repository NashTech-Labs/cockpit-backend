#!/bin/bash
sudo chmod 666 /var/run/docker.socket
sudo docker-compose -f /temp/nginx/docker-compose.yaml start