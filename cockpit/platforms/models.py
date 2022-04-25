from django.db import models
from django.db import connections


# Create your models here.

class Instance(models.Model):

    INSTANACE_STATE = [
        ('P','PENDING'),
        ('R','RUNNING'),
        ('S','STOPPED'),
        ('T','TERMINATED')
    ]
    platform_id= models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=255,blank=False,null=False)
    public_ip = models.CharField(max_length=255,blank=True,default="None")
    private_ip = models.CharField(max_length=255,null=False,default="None")
    instance_state = models.CharField(max_length=255,null=False,default='pending')
    platform = models.CharField(max_length=255,blank=True,default='None')
    platform_state= models.IntegerField(blank=True)
    guacamole_ws_url= models.CharField(max_length=255,blank=True,null=True,default='None')
    guacamole_sharing_url = models.CharField(max_length=255,blank=True,null=True,default='None')

    class Meta:
        db_table = "instance"    

    objects = models.Manager()

    def __str__(self):
        return self.instance_id

class AwsEc2Details(models.Model):
    image_id=models.CharField(max_length=255,primary_key=True)
    instance_type=models.CharField(max_length=255,default='t2.micro')
    subnet_id = models.CharField(max_length=255,null=False, blank=False)
    security_group_id = models.CharField(max_length=255)
    iam_profile = models.CharField(max_length=255)
    key_name = models.CharField(max_length=255)
    platforms = models.CharField(max_length=255)

    class Meta:
        db_table = "aws_ec2_details"

    objects = models.Manager()

    def __str__(self):
        return self.image_id


cursor = connections['default'].cursor()  #Allows Python code to execute PostgreSQL command in a database session
cursor.execute("INSERT INTO aws_ec2_details(image_id,instance_type,subnet_id,security_group_id,iam_profile,key_name,platforms) VALUES ('i-01', 't2.micro','sub-234','sg-01','iam','hello.pem','jenkins')")
