from django import forms
from .models import Freelancer

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['name', 'email', 'username', 'password', 'skills']
