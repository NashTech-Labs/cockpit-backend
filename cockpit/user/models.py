from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250, primary_key=True)