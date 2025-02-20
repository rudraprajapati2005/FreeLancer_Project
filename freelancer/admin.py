from django.contrib import admin

# Register your models here.
from .models import Freelancer, Client

admin.site.register(Freelancer)
admin.site.register(Client)