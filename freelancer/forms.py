from django import forms
from .models import Freelancer, AboutFreelancer, Client, Project, Users, Bid
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

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'amount',
            'delivery_time',
            'proposal_text',
            'proposal_highlights',
            'technical_approach',
            'milestone_breakdown',
            'attachments'
        ]
        
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your bid amount',
                'min': '0',
                'step': '0.01'
            }),
            'delivery_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of days to complete',
                'min': '1'
            }),
            'proposal_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your detailed proposal',
                'rows': 5
            }),
            'proposal_highlights': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Key points of your proposal (optional)',
                'rows': 3
            }),
            'technical_approach': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your technical approach (optional)',
                'rows': 3
            }),
            'milestone_breakdown': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Break down your delivery milestones (optional)',
                'rows': 3
            }),
            'attachments': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            })
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if 'project' in self.initial:
            project = self.initial['project']
            if amount < project.budget:
                raise forms.ValidationError("Bid amount cannot be less than project budget")
        return amount