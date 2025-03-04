from django.db import models
from django.contrib.auth.models import User
class Freelancer(models.Model):
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    skills = models.TextField()  # Store the skills as a comma-separated string

class   Photo(models.Model):
    username=models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to='photos/profile_pic')

class Client(models.Model):
    name = models.CharField(max_length=255,unique=False)
    companyname = models.CharField(max_length=255,null=False,blank=False)
    address = models.CharField(max_length=1024,blank=False,null=False)
    state = models.CharField(max_length=255,blank=False, null=False)
    businessEmail = models.EmailField(unique=True)
    phone = models.TextField(max_length=15, null=False,blank=False)


STATUS_CHOICES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('closed', 'Closed'),
]

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return self.title
    
    def is_active(self):
        return self.status == 'open'