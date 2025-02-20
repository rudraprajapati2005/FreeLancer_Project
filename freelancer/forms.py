from django import forms
from .models import Freelancer
from .models import Client
class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['name', 'email', 'username', 'password', 'skills']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'companyname', 'address', 'state', 'businessEmail', 'phone']
