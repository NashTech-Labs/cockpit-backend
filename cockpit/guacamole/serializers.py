from django.core import serializers
import json
from .models import GuacamoleConnectionParameter
import logging


#GET GUACAMOLE CONNECTIONS DETAILS GET

logger= logging.getLogger(__name__)
def get_connection_details(instance_ip=None):
    """returns guacamole connection details based on instance_ip if it exits in db 
    else return None 
    """
    try:
        data = json.loads(serializers.serialize('json', GuacamoleConnectionParameter.objects.using('guacamole_db').filter(
            parameter_value=instance_ip),
            fields=(
                "connection",
                "parameter_name",
                "parameter_value"
                )
            )
        )
        if len(data) !=0:
            for connection_obj in data:

                if connection_obj["fields"]["parameter_value"] == instance_ip :
                    temp_dict_obj=connection_obj["fields"]
                    connection_id={"connection_id":"{}".format(connection_obj['pk'])}
                    temp_dict_obj.update(connection_id)
                    return  temp_dict_obj
        return {}
    except Exception as e:
        logger.error("Exception--> {}".format(e))
        return {}

# if __name__ == "__main__":
#     get_connection_details(instance_ip="openssh-server")
    #json.loads(serializers.serialize('json', GuacamoleConnectionParameter.objects.using('guacamole_db').all()))