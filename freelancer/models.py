from django.db import models

class Freelancer(models.Model):
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    skills = models.TextField()  # Store the skills as a comma-separated string

    
