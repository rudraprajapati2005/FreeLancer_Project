from django import forms
from .models import Freelancer,Photo

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['name', 'email', 'username', 'password', 'skills']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['username', 'image']
