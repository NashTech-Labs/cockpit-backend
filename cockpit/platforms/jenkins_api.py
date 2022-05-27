import logging
import platform
import subprocess
import xml.etree.ElementTree as ET
import jenkins
import requests
import urllib,os


class JenkinsJobBuilderExecutable(object):
    """
    wrapper for executing jjb CLI commands
    """
    PATH = 'executable_path'

    def __init__(self, server, username, password,executable_path=None,):
        """
        :param machine_readable:
        :param config:
        """
        self.server = server
        self.username = username
        self.password = password
        self.client = jenkins.Jenkins(  self.server,
                                        username=self.username, 
                                        password=self.password
                                )
        self.log = logging.getLogger(self.__class__.__name__)
        self.token = os.getenv("JENKINS_TOKEN","")

        # default configuration
        self.configuration = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            JenkinsJobBuilderExecutable.PATH: 'packer.exe' if 'Windows' == platform.system() else '/usr/bin/jenkins-jobs'
        }

        # add overrides
        if executable_path:
            self.configuration[JenkinsJobBuilderExecutable.PATH] = executable_path

    def generate_xml(self, template, output,**kwargs):
    
        exit_status,log,err=self.execute_cmd("test", template, output,**kwargs)
        if exit_status == 0:
            return "{}/config.xml".format(output)
        else:
            return None


    def execute_cmd(self, jjb_cmd, template=None, output=None, **kwargs):
        cmd_args = list()
        cmd_args.append(self.configuration[JenkinsJobBuilderExecutable.PATH])
        cmd_args.append(jjb_cmd)
        cmd_args.append(template)
        cmd_args.append("-o{0}".format(output))
        cmd_args.append("--config-xml")
        
        print("CMD_ARG  {}".format(cmd_args))
        p = subprocess.Popen(cmd_args, stdin=subprocess.PIPE,
                             stdout=self.configuration['stdout'], stderr=self.configuration['stderr'])
        out, err = p.communicate()

        return p.returncode, out, err

    def create_job(self,configxml,pipelinename):
        try:
            tree = ET.parse("{0}/config.xml".format(configxml))
            root = tree.getroot()
            xml_data=ET.tostring(root, encoding='utf8', method='xml').decode()

            self.client.create_job(pipelinename, xml_data)
            
        except Exception as e:
            print("Error jenkins creating job \n{}".format(e))

    def create_credential(self,credusername,credpassword):
        REST_API="http://{0}:{1}@{2}//credentials/store/system/domain/_/createCredentials".format(self.username,
                                                self.token,
                                                self.server[7:])
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}                                        
        payload={'json':{
            "": "0",
            "credentials": {
                "scope": "GLOBAL",
                "id": "git-{}".format(credusername),
                "username": credusername,
                "password": credpassword,
                "description": "Git Cred for user:{}".format(credusername),
                "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"
            }
        }}
        r = requests.post(
            data=urllib.parse.urlencode(payload),
            url=REST_API,
            headers=headers
        )
        return r


        