from django.db import models

class Freelancer(models.Model):
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    skills = models.TextField()  # Store the skills as a comma-separated string

    

    
class   Photo(models.Model):
    #python -m pip install Pillow , if PIllow is not Installed
    username=models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to='photos/profile_pic')

class Client(models.Model):
    name = models.CharField(max_length=255,unique=False)
    companyname = models.CharField(max_length=255,null=False,blank=False)
    address = models.CharField(max_length=1024,blank=False,null=False)
    state = models.CharField(max_length=255,blank=False, null=False)
    businessEmail = models.EmailField(unique=True)
    phone = models.TextField(max_length=15, null=False,blank=False)