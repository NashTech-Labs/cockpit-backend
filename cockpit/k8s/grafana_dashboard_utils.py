from grafana_api.grafana_face import GrafanaFace
import os

def _get_grafana_client(auth=os.getenv('GRAFANA_API_TOKEN','None'),host=os.getenv('GRAFANA_HOST','localhost:3000')):
    grafana_client = GrafanaFace(
                    auth=auth, 
                    host=host
                )
    return grafana_client

def create_prometheus_datasource(prometheus_endpoint,datasource_name):

    try:
        data_source={
            "name":"{}".format(datasource_name),
            "type":"prometheus",
            "access":"proxy",
            "url":"{}".format(prometheus_endpoint),
            "basicAuth":False,
            "isDefault":False,
            "jsonData":{
                "httpMethod":"POST"
            },
            "version":2,
            "accessControl":{
                "alert.instances.external:read":True,
                "alert.instances.external:write":True,
                "alert.notifications.external:read":True,
                "alert.notifications.external:write":True,
                "alert.rules.external:read":True,
                "alert.rules.external:write":True,
                "datasources.id:read":True,
                "datasources:delete":True,
                "datasources:query":True,
                "datasources:read":True,
                "datasources:write":True
            }
        }
        grafana_client=_get_grafana_client()
        response=grafana_client.datasource.create_datasource(data_source)
        return response
    except Exception as e:
        print("Error creating datasources :{}".format(e))
        response={
            'id':"None",
            'uid': "None",
            'name':'{}'.format(datasource_name),
            'type':'prometheus',
            'message':'Datasource creation failed',
        }
        return response