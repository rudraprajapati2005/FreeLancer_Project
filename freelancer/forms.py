from django import forms
from .models import Freelancer, AboutFreelancer, Client, Project, Users
from datetime import date

class FreelancerForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['skills']
        required = False

        widgets = {
            'skills': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your skills'}),
        }

class AboutFreelancerForm(forms.ModelForm):
    class Meta:
        model = AboutFreelancer
        fields = ['image', 'about_freelancer', 'gitLinks', 'links', 'experience']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['companyname', 'address', 'state', 'businessEmail']

        widgets = {
            'companyname': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Company Name if any'}),
            'address': forms.Textarea(attrs={'class': 'input-textarea', 'placeholder': 'Write the Full Address', 'required': 'required'}),
            'state': forms.Select(attrs={'class': 'input-select'}),
            'businessEmail': forms.EmailInput(attrs={'class': 'input-text', 'required': 'required'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'skills_required', 'budget', 'deadline', 'status']
        
        CATEGORY_CHOICES = [
            ('web_development', 'Web Development'),
            ('mobile_app', 'Mobile App Development'),
            ('design', 'Design'),
            ('writing', 'Writing & Translation'),
            ('admin', 'Admin Support'),
            ('marketing', 'Marketing'),
            ('other', 'Other')
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-title',
                'placeholder': 'Enter project title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-description',
                'placeholder': 'Describe your project requirements',
                'required': True
            }),
            'category': forms.Select(choices=CATEGORY_CHOICES, attrs={
                'class': 'form-category',
                'required': True
            }),
            'skills_required': forms.TextInput(attrs={
                'class': 'form-skills',
                'placeholder': 'Search and select required skills',
                'required': True,
                'id': 'searchProjectSkills'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-budget',
                'min': '0',
                'step': '0.01',
                'required': True
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-deadline',
                'required': True,
                'min': date.today().strftime('%Y-%m-%d')  # Set minimum date to today
            }),
            'status': forms.Select(attrs={
                'class': 'form-status',
                'required': True
            })
        }

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'email', 'username', 'password', 'phone']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'input-text', 'placeholder': 'Enter your email', 'required': 'required'}),
            'username': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Enter your username', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'input-text', 'placeholder': 'Enter your password', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'input-text', 'pattern': '^[6789][0-9]{9}$', 'placeholder': 'Enter your phone number'}),
        }