from django.db import models

# Create your models here.

class Instance(models.Model):
    INSTANACE_STATE = [
        ('P','PENDING'),
        ('R','RUNNING'),
        ('S','STOPPED'),
        ('T','TERMINATED')
    ]
    instance_id = models.CharField(max_length=255,primary_key=True,notnull=True)
    public_ip = models.CharField(max_length=255,blank=True)
    private_ip = models.CharField(max_length=255,notnull=True)
    instance_state = models.CharField(max_length=255,notnull=True,choices=INSTANACE_STATE,default='PENDING')
    platforms = models.CharField(max_length=255,blank=True)
    platforms_state= models.IntegerField(blank=True)