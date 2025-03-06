from django.contrib import admin
from .models import Freelancer,Client,Photo,Users
# Register your models here.

admin.site.register(Freelancer)
admin.site.register(Client)
admin.site.register(Photo)
admin.site.register(Users)