from django import forms
from .models import Freelancer, Photo, Client

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['name', 'email', 'username', 'password', 'skills']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['username', 'image']

        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'companyname', 'address', 'state', 'businessEmail', 'phone']