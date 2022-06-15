import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from kubernetes.client import ApiClient



def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = kubernetes.client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance1 = kubernetes.client.CoreV1Api(api_client)
        return api_instance1

    except ApiException as e:
        print("Error getting kubernetes client:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return None

def __format_data_for_create_cronjob(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        #print("JSON_DATA OF KUBERNETES OBJECT:{}".format(json_data))
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list


def get_namespace(cluster_details):

    try:
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        res=client_api.list_namespace()

        data=__format_data_for_create_cronjob(res)
        print(data) 
        # print("list of all namespaces :{}".format(res))
    except ApiException as e:
        print("ERROR IN getting_namespace:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))



def create_namespace(cluster_details,namespace):

    try:
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        res=client_api.create_namespace(
            client.V1Namespace(
                metadata=client.V1ObjectMeta(name=namespace)
        
            ))

        print("namespace created. status='%s'" % str(res.status))

    except ApiException as e:
        print("ERROR IN creating_namespace:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))




def delete_namespace(cluster_details,namespace):

    try:
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
            )

        res=client_api.delete_namespace(namespace)
        print(res)

    except ApiException as e:
        print("ERROR IN deleting_namespace:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))



if __name__ == '__main__':
    batch_v1 = client.BatchV1Api()
    cluster_details={
        "bearer_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IlYxVWh2RUFSYnZPX1Nka0VTdExRVUNpYnhhdnR5WVNQVmtuYXdMMGFyekUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRhc2hib2FyZC1jbHVzdGVyLXJvbGUtdG9rZW4tbXN3bngiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWNsdXN0ZXItcm9sZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjJmZTVkNjg4LWM5NjAtNDE4Yy04MWEyLTcyNTJiZDIwNWRhNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRhc2hib2FyZC1jbHVzdGVyLXJvbGUifQ.t7gBKdpf6jZNXLswm3aHS_3Gu_PLzuLVBVLx_4gOcxHkyaIJ-vJFj8gSVzSBAmW56D3Rq_tpSVAWPauXv4Cca11PJ9O3ZI_6yuCDRXZre7EcmFDOPrlTjQwH-63mH4ItdWMwqLD2HXABOtnRUwrtSMwBIurZJ53_U_O--XUFo9kxTGqMAyeNY7kCACutHwZeCIXchYQ9WMku01vKLcSyV4p5SdK3Wk6ek-CbyN4fScSfQStgsFN37CV2ssNZTThbi3PXzXVMuKnUQXUzYLSwe46kvvLGnaCIYqRgxWpGMSnHlh--pws73-QKLRFmvO_HOLFDnBOe_06yEJ8i47YP9Q",
        "api_server_endpoint":"https://34.123.166.9"
    }
    
    # create_namespace(cluster_details,"n1")
    # delete_namespace(cluster_details, "n1")
    get_namespace(cluster_details)
