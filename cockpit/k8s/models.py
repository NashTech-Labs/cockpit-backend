from django.db import models


class KubernetesConfig(models.Model):
    bearer_token = models.TextField(blank=True,null=True,default='None')
    version= models.CharField(max_length=255,blank=True,default="None")
    cluster_name= models.CharField(max_length=255,blank=True,default="None")
    api_server_endpoint = models.TextField(blank=True,null=True,default='None')
    kubeconfig = models.TextField(blank=True,null=True,default='None')
    cloud= models.CharField(max_length=255,blank=True,default="None")
    enable_monitoring=models.CharField(max_length=255,blank=True,default="false")

    class Meta:
        db_table = "kubernetes_config"
    objects = models.Manager()

    def __str__(self):
        return self.version

class MonitoringConfig(models.Model):
    cluster_name= models.CharField(max_length=255,blank=True,default="None")
    prometheus_server_url=models.TextField(blank=True,null=True,default='None')
    grafana_dashboard_url=models.TextField(blank=True,null=True,default='None')
    monitoring_state=models.IntegerField(blank=True,default=4000)
    message = models.TextField(blank=True,null=True,default='None')
    grafana_prometheus_datasource_name=models.CharField(max_length=255,blank=True,default="None")
    grafana_prometheus_datasource_uid=models.CharField(max_length=255,blank=True,default="None")



    class Meta:
        db_table = "monitoring_config"
    objects = models.Manager()

    def __str__(self):
        return self.version
