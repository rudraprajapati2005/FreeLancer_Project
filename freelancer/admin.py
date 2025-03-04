from django.contrib import admin
from .models import Freelancer,Client,Photo
# Register your models here.
admin.site.register(Freelancer)
admin.site.register(Client) 
admin.site.register(Photo)