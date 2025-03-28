from django.db import models
from django.core.validators import RegexValidator

class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=[('client', 'Client'), ('freelancer', 'Freelancer')])
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.username

class Freelancer(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='freelancer_profile')
    skills = models.TextField()
    
    def __str__(self):
        return self.user.username

class AboutFreelancer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='AboutFreelancers/profile_pic')
    about_freelancer = models.TextField(null=True, blank=True)
    gitLinks = models.TextField(null=True, blank=True)
    links = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='about_freelancer', null=True, blank=True)

    def __str__(self):
        return f"{self.freelancer.user.username}'s Profile"

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
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='client_profile')
    image = models.ImageField(upload_to='Client/profile_pic', null=True, blank=True)
    companyname = models.CharField(max_length=255)
    address = models.TextField(max_length=1024)
    state = models.CharField(max_length=255, choices=INDIAN_STATES)
    businessEmail = models.EmailField()

    def __str__(self):
        return self.user.username

STATUS_CHOICES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('closed', 'Closed'),
]

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    posted_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='posted_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

