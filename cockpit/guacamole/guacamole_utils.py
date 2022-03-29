from guacapy.client import Guacamole
from guacapy.templates import *
from .guacamole_connections import *
import os 

try:
    __guacamole_client = Guacamole(
            os.getenv("GUACAMOLE_HOST","localhost:49154/"),
            os.getenv("GUACAMOLE_USERNAME","guacadmin"),
            os.getenv("GUACAMOLE_PASSWORD","guacadmin"),
            method='http',
            url_path='guacamole'
        )
except Exception as e:
    print("Error in Guacamole client object creattion {}".format(e))

def _get_formatted_connection_data(connection_json, connection_type='ssh'):
    """returns formatted dictionary object"""
    try:
        if connection_type == 'ssh':
            return get_ssh_connection(connection_json)
        else:
            print("Connection type {} not supported".format(connection_type))
            return None
    except Exception as e:
        print("Error in formatting ssh payload \nError {}".format(e))
        return None

def get_guacamole_token():

    """Returns the guacamole api token"""
    try:
        return __guacamole_client.token
    except Exception as e:
        print("Error in getting guacamole api token {}".format(e))
        return None

def create_guacamole_connection(connections_details):
    """Creats the connection in guacamole datasource
    example connections details
    {
        'name' : 'something_unique'
        'hostname' : "0.0.0.0",
        'port' : '22',
        'protocol' : 'ssh',
        'username' : 'ubuntu',
        'password' : 'trynexttime',
        'private-key' : ''
    }
    """
    
    try:
        payload=_get_formatted_connection_data(connections_details,connection_type=connections_details["protocol"])
        response=__guacamole_client.add_connection(payload)
        return response
    except Exception as e :
        print("Error in creating connection to guacamole \nError:{}".format(e))
        return None

def create_sharing_profile(connection_details):
    """creates sharing profile with write access
    example payload
        {
            "primaryConnectionIdentifier":"4",
            "name":"sachin",
            "parameters":{
                "read-only":""
            },
            "attributes":{}
        }
    """
    try:
        sharing_profile_payload={
            "primaryConnectionIdentifier":"{}".format(connection_details["identifier"]),
            #unique name
            "name":"{}".format(connection_details["name"]),
            "parameters":{
                "read-only":""
            },
            "attributes":{}
        }
        response=__guacamole_client.add_sharing_profile(sharing_profile_payload)
        return response
    except Exception as e :
        print("Error in creating sharing profile to guacamole \nError:{}".format(e))
        return None


    
#data=    { 'name' : 'something_unique''hostname' : "0.0.0.0",'port' : '22''protocol' : 'ssh','username' : 'ubuntu''password' : 'trynexttime','private-key' : ''}
#a={"primaryConnectionIdentifier":"6","name":"sachin","parameters":{"read-only":""},"attributes":{}}