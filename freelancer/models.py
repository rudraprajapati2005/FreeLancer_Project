from django.db import models

# Create your models here.

#table for storing different freelancer details:

class freelancer_detail(models.Model):
    freelancer_id=models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=25)
    name=models.CharField(max_length=50)
    