from .guacamole_client import Guacamole
from .guacamole_template import *
from .guacamole_connections import *
from cockpit.celery import app 
import os 
import websocket
import time

#websocket.enableTrace(True)

try:
    __guacamole_client = Guacamole(
            os.getenv("GUACAMOLE_HOST","localhost:8080"),
            os.getenv("GUACAMOLE_USERNAME","guacadmin"),
            os.getenv("GUACAMOLE_PASSWORD","guacadmin"),
            method='http',
            url_path='/guacamole'
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
        return {}

def create_sharing_profile(connection_details):
    """creates sharing profile with write access

    payload to function
    {'identifier': "ID", "name": "writeacess"}

    example payload to GUACAMOLE API
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
        return {}

def __get_connection_websocket_url(connection_id):
    #'ws://localhost:8080/guacamole/websocket-tunnel?token=F6DB724E26B06A6B5E726616E938285432E0FEBD16A85E0FCB9FED81BB50687A&GUAC_DATA_SOURCE=postgresql&GUAC_ID=1&GUAC_TYPE=c&GUAC_WIDTH=575&GUAC_HEIGHT=667&GUAC_DPI=105&GUAC_TIMEZONE=Asia%2FCalcutta&GUAC_AUDIO=audio%2FL8&GUAC_AUDIO=audio%2FL16&GUAC_IMAGE=image%2Fjpeg&GUAC_IMAGE=image%2Fpng&GUAC_IMAGE=image%2Fwebp')
    try:
        GUAC_DATA_SOURCE='postgresql'
        GUAC_ID='{}'.format(connection_id)
        GUAC_TYPE='c'
        GUAC_WIDTH=575
        GUAC_HEIGHT=667
        GUAC_DPI=105
        GUAC_TIMEZONE='Asia%2FCalcutta'
        GUAC_AUDIO='audio%2FL8'
        GUAC_AUDIO_1='audio%2FL16'
        GUAC_IMAGE='image%2Fjpeg'
        GUAC_IMAGE_1='image%2Fpng'
        GUAC_IMAGE_2='image%2Fwebp'
        TOKEN=__guacamole_client.token
        
        connection_parameters="token={0}&GUAC_DATA_SOURCE={1}&GUAC_ID={2}&GUAC_TYPE={3}&GUAC_WIDTH={4}&GUAC_HEIGHT={5}&GUAC_DPI={6}&GUAC_TIMEZONE={7}&GUAC_AUDIO={8}&GUAC_AUDIO={9}&GUAC_IMAGE={10}&GUAC_IMAGE={11}&GUAC_IMAGE={12}".format(
            TOKEN,
            GUAC_DATA_SOURCE,
            GUAC_ID,
            GUAC_TYPE,
            GUAC_WIDTH,
            GUAC_HEIGHT,
            GUAC_DPI,
            GUAC_TIMEZONE,
            GUAC_AUDIO,GUAC_AUDIO_1,
            GUAC_IMAGE,GUAC_IMAGE_1,GUAC_IMAGE_2
        )
        websocket_connection_url="ws://{0}/guacamole/websocket-tunnel?{1}".format(
            os.getenv("GUACAMOLE_HOST","localhost:8080"),
            connection_parameters
            )
        return { "URL": "{}".format(websocket_connection_url) }
    except Exception as e:
        print("Error in get_connection_websocket_url \nError: {}",format(e))
        return {}

@app.task(time_limit=3600,queue='guacamole')
def __create_active_websocket_connection(payload):
    try:
        websocket.enableTrace(True)
        w_socket = websocket.WebSocket()
        if len(payload) != 0:
            w_socket.connect(payload["URL"])
            while(True):
                time.sleep(1)
                data="3.key,5.65293,1.0;"
                w_socket.send(data)
    except Exception as e:
        print("Error in create_active_websocket_connection \n{}".format(e))

def get_active_connection_details(connection_details):
    try:

        if len(connection_details) != 0:
            
            PAYLOAD_URL=__get_connection_websocket_url(connection_details["identifier"])
            print("PAYLOAD URL: {}".format(PAYLOAD_URL))
            __create_active_websocket_connection.delay(PAYLOAD_URL)
            time.sleep(1)
            
            active_connection_details=__guacamole_client.get_active_connections()

            for act_con in active_connection_details:
                print("active_connevction: {}".format(active_connection_details[act_con]))
                act_con_details=active_connection_details[act_con]

                if act_con_details['connectionIdentifier'] == connection_details["identifier"]:
                    return act_con_details["identifier"],PAYLOAD_URL
        else:
            return None

    except Exception as e:
        print("Error in get_active_connection_details \nError: {}".format(e))
        return None
    
def get_sharing_profile_url(active_connection_id,connection_id):

    try:
        #active_connection_details=get_active_connection_details(active_connection)
        
        sharing_credentials=__guacamole_client.get_sharing_profile_credential(active_connection_id,connection_id)
        keys=sharing_credentials.keys()
        #keys.sort()

        if 'values' in keys:
            credentials_key=sharing_credentials['values']['key']
            URL="http://{0}/guacamole/#/?key={1}".format(
                os.getenv("GUACAMOLE_SHARING_HOST","localhost:8080"),
                credentials_key
                )
            print("SHARING_URL: {}".format(URL))
            return URL
        else: 
            return None

    except Exception as e:
        print("Error in get_sharing_profile_url \nError: {}".format(e))
        return None

def paltform_guacamole(instance_data):
    try:
        connection_details=create_guacamole_connection(instance_data)

        if len(connection_details) != 0:

            profile=create_sharing_profile(connection_details)

            print("\n profile :{}".format(profile))

            sharing_profile_id=profile['identifier']

            active_connections_id,WS=get_active_connection_details(connection_details)
            if active_connections_id is not None:
            #SHARING_PROFILE_URL=get_sharing_profile_url(active_connections_id,sharing_profile_id)
                return {"URL":"{}".format(get_sharing_profile_url(active_connections_id,sharing_profile_id))},WS
            else :
                return {"URL": None}
        else:
            return {"URL": None}        
    except Exception as e:
        print("Error in paltform_guacamole {}".format(e))
        return {"URL": None}  
