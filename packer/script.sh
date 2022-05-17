#!/bin/bash

echo $PWD
whoami

sudo apt update &> /dev/null
sudo apt install unzip -y &> /dev/null

sudo curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo unzip awscliv2.zip > /dev/null
sudo ./aws/install > /dev/null 2>&1

export PATH="/usr/local/bin/aws:${PATH}"


sudo aws s3 cp s3://cockpit010/nginx /temp/nginx --recursive
cd /temp/nginx
sudo chmod +x startup.sh
sudo sh startup.sh

#sudo sed -i "s/_DOMAINNAME_/`ec2metadata --public-ipv4`/g" data/jenkins.conf 

sudo apt-get update && sudo apt install -y docker.io > /dev/null
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

sudo docker-compose --version

sudo systemctl enable  startup.service