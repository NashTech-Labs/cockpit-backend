from django.db import models

# Create your models here.

class ArgocdConfig(models.Model):
    bearer_token = models.TextField(blank=True,null=True,default='None')
    git_url = models.TextField(blank=True,null=True,default='None')
    username = models.CharField(max_length=255,blank=True,default="None")
    password = models.CharField(max_length=255,blank=True,default="None")
    api_server_endpoint = models.TextField(blank=True,null=True,default='None')
    cluster_name= models.CharField(max_length=255,blank=True,default="None")

    class Meta:
        db_table = "argocd_config"
    objects = models.Manager()

    def __str__(self):
        return self.version