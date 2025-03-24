from django import forms
from .models import Freelancer, AboutFreelancer, Client,Project,Users

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['name', 'email', 'username', 'password', 'skills']

class AboutFreelancerForm(forms.ModelForm):
    class Meta:
        model = AboutFreelancer
        fields = ['username', 'image']

 
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','username', 'companyname', 'address', 'state', 'businessEmail','phone','password']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'YOUR NAME', 'required': 'required'}),
            'username': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your username', 'required': 'required'}),
            'companyname': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Company Name if any'}),
            'address': forms.Textarea(attrs={'class': 'input-textarea', 'placeholder': 'Write the Full Address', 'required': 'required'}),
            'state': forms.Select(attrs={'class': 'input-select'}),
            'businessEmail': forms.EmailInput(attrs={'class': 'input-text', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'input-text', 'pattern': '^[6789][0-9]{9}$', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'input-text', 'required': 'required'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'skills_required', 'budget', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-title'}),
            'description': forms.Textarea(attrs={'class': 'form-description'}),
            'category': forms.Select(attrs={'class': 'form-category'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-skills'}),
            'budget': forms.NumberInput(attrs={'class': 'form-budget'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-deadline'}),
            'status': forms.Select(attrs={'class': 'form-status'}),
        }

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'email', 'username', 'password', 'user_type']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'input-text', 'placeholder': 'Enter your email', 'required': 'required'}),
            'username': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your username', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'input-text', 'placeholder': 'Enter your password', 'required': 'required'}),
            'user_type': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter the user type', 'required': 'required'}),
        } 