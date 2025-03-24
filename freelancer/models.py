from django.db import models
from django.contrib.auth.models import User
class Freelancer(models.Model):
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    skills = models.TextField()  # Store the skills as a comma-separated string

class   AboutFreelancer(models.Model):
    username=models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to='AboutFreelancers/profile_pic')
    about_freelancer=models.TextField(null=True )
    gitLinks=models.TextField(null=True)
    links=models.TextField(null=True)
    freelancer = models.ForeignKey(Freelancer, to_field='username', on_delete=models.CASCADE, related_name='about_freelancer',null=True,blank=True)

       
INDIAN_STATES = [
    ('', 'Select State'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Puducherry'),
]
class Client(models.Model):
    username=models.CharField(max_length=255,unique=True,blank=True, null=True)
    name = models.CharField(max_length=255,unique=False)
    companyname = models.CharField(max_length=255,null=False,blank=False)
    address = models.TextField(max_length=1024,blank=False,null=False)
    state = models.CharField(max_length=255,choices=INDIAN_STATES,blank=False, null=False)
    businessEmail = models.EmailField(unique=False)
    phone=models.CharField(max_length=10,unique=False)
    password = models.CharField(max_length=255,null=False,blank=False,default='password')

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

    
class freelancer_additional_details(models.Model):
    freelancer=models.ForeignKey(Freelancer,to_field='username',on_delete=models.CASCADE)
    about=models.TextField(unique=False)
    links=models.TextField(unique=False)
    experience=models.TextField(unique=False)

class Users(models.Model):
    name=models.CharField(max_length=255,unique=False)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255,unique=False)

