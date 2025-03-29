from django.contrib import admin
from .models import Freelancer, Client, AboutFreelancer, Users, Project, Bid
# Register your models here.

admin.site.register(Freelancer)
admin.site.register(Client)
admin.site.register(AboutFreelancer)
admin.site.register(Users)
admin.site.register(Bid)
admin.site.register(Project)

