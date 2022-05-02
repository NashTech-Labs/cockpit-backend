from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=250, blank=False)
    user_email = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "user"

    objects = models.Manager()

    def __str__(self):
        return self.username