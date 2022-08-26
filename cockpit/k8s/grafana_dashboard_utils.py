from grafana_api.grafana_face import GrafanaFace
import os
from grafanalib._gen import DashboardEncoder
import json
import requests

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
        return response['datasource']
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

def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    return json.dumps(
        {
            "dashboard": dashboard,
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)


def create_grafana_dashboard(json, verify=True):
    try:
        server=os.getenv('GRAFANA_HOST','localhost:3000')
        api_key=os.getenv('GRAFANA_API_TOKEN','None')
        headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
        r = requests.post(f"http://{server}/api/dashboards/db", data=json, headers=headers, verify=verify)
        # TODO: add error handling
        print(f"{r.status_code} - {r.content}")
        if r.status_code == 200:
            dashboard = r.json()
            return dashboard
        else:
            dashboard={
                "id":-1,
                "slug":"None",
                "status":"failed",
                "uid":"None",
                "url":"None",
                "version":2
            }
            return dashboard
    except Exception as e:
        print("Error in Creating Dashboard:\n{}".format(e))
        dashboard={
                "id":-1,
                "slug":"kNone",
                "status":"failed",
                "uid":"None",
                "url":"None",
                "version":2
            }
        return dashboard

def generated_dashboard_url(prometheus_datasource=None):
    try:
        dashboard_info={
            "grafana_k8s_apiserver_dashboard_url":"",
            "grafana_k8s_apiserver_dashboard_uid":"",
            "grafana_k8s_apiserver_dashboard_id":"",
            "grafana_k8s_container_dashboard_url":"",
            "grafana_k8s_container_dashboard_uid":"",
            "grafana_k8s_container_dashboard_id":"",
            "monitoring_state": 4010
        }
        dashboards_list=[
            "/grafana_dashboard/k8s_api_server.json",
            "/grafana_dashboard/k8s_container.json"
            ]
        for dashboard in dashboards_list:
            with open(dashboard,'r') as file_obj:
                data = json.loads(file_obj.read())
                for variables in data['templating']['list']:
                    if variables['name'].lower() == 'datasource':
                        variables.update(regex='{}'.format(prometheus_datasource))
                        break
                    else:
                        print("datasource variables not found")
                my_dashboard_json = get_dashboard_json(data, overwrite=True)
                dashboard_data=create_grafana_dashboard(my_dashboard_json)
                if dashboard == "/grafana_dashboard/k8s_api_server.json" :
                    dashboard_info.update(
                        grafana_k8s_apiserver_dashboard_url="http://{0}{1}".format(os.getenv('GRAFANA_HOST','localhost:3000'),dashboard_data['url']),
                        grafana_k8s_apiserver_dashboard_uid='{}'.format(dashboard_data['uid']),
                        grafana_k8s_apiserver_dashboard_id='{}'.format(dashboard_data['id'])
                    )
                else:
                    dashboard_info.update(
                        grafana_k8s_container_dashboard_url="http://{0}{1}".format(os.getenv('GRAFANA_HOST','localhost:3000'),dashboard_data['url']),
                        grafana_k8s_container_dashboard_uid='{}'.format(dashboard_data['uid']),
                        grafana_k8s_container_dashboard_id='{}'.format(dashboard_data['id'])
                    )
        return dashboard_info
    except Exception as e:
        print("Error in getting dashboard url \n{}".format(e))
        dashboard_info={
            "grafana_k8s_apiserver_dashboard_url":"None",
            "grafana_k8s_apiserver_dashboard_uid":"None",
            "grafana_k8s_apiserver_dashboard_id":"None",
            "grafana_k8s_container_dashboard_url":"None",
            "grafana_k8s_container_dashboard_uid":"None",
            "grafana_k8s_container_dashboard_id":"None",
            "monitoring_state":4011
        }
        return dashboard_info