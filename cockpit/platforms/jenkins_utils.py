import jenkins
import os
import pout
import xml.etree.ElementTree as ET

# function for creating jenkins client
def create_jenkins_client(jenkinsurl,un,passwd):

    client = jenkins.Jenkins(jenkinsurl, 
    username=un, password=passwd)
    return client

#Conveting .xml file to string
def convert_xml_file_to_str():
    tree = ET.parse('/home/knoldus/python-jenkins/config.xml')
    root = tree.getroot()
    return ET.tostring(root, encoding='utf8', method='xml').decode()

# function to create jenkins job using custom config.xml
def create_jenkins_job(config,client):
    client.create_job('pipeline-job3', config)
    pout.v(config)


config = convert_xml_file_to_str()
client=create_jenkins_client(jenkinsurl='http://localhost:8080',un='admin',
    passwd='admin')
create_jenkins_job(config,client)



