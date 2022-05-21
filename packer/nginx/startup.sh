#!/bin/bash

#run-jenkins.sh
sudo cp /temp/nginx/run-jenkins.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/run-jenkins.sh

sudo cp /temp/nginx/startup.service /etc/systemd/system/
sudo chmod 640 /etc/systemd/system/startup.service

sudo systemctl status startup.service
sudo systemctl daemon-reload

sudo systemctl enable  startup.service
sudo systemctl status startup.service



