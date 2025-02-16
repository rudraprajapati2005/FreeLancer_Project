from django.shortcuts import render,HttpResponse
from .models import Freelancer

# Create your views here.
def home(request):
    return render(request,'user/main_page.html')

# def freelancer_signup(request):
#     return render(request,'freelancer/freelancer_signup.html')

def client_signup(request):
    return render(request,'client/client_signup.html')

def client_home_page(request):
    return render(request,'client/client_pov.html')

def client_add_project(request):
    return render(request,"client/add_project_client.html")

from django.shortcuts import render, redirect
from .forms import FreelancerForm

def freelancer_signup(request):
    if request.method == "POST":
        form = FreelancerForm(request.POST)
        if form.is_valid():
            freelancer = form.save(commit=False)
            # Process the skills field
            skills = request.POST.getlist('skills')
            freelancer.skills = ','.join(skills)
            freelancer.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = FreelancerForm()
    return render(request, 'freelancer/freelancer_signup.html', {'form': form})

def show_details_freelancer(request):
    error={}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        if Freelancer.objects.filter(username=username).exists():
            error['error_username'] = 'Username already exists'
            return render(request, 'freelancer/freelancer_signup.html',error)

        password = request.POST.get('password')
        selected_skills = request.POST.get('selected_skills')

        # Create a new Freelancer object and save it to the database
        freelancer = Freelancer(
            name=name,
            email=email,
            username=username,
            password=password,
            skills=selected_skills
        )
        freelancer.save()
        freelancer.__dict__
        return render(request,'freelancer/freelancer_homepage.html')
    return render(request, 'freelancer_signup.html')