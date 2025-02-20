from django.shortcuts import render,HttpResponse
from .models import Freelancer,Photo
from .forms import PhotoForm,FreelancerForm
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
    freelancer_details={}
    username = request.POST.get('username')
    email = request.POST.get('email')    
    if request.method == 'POST':
        name = request.POST.get('name')
        request.session['name']=name
        email = request.POST.get('email')
        request.session['email']=email
        username = request.POST.get('username')
        request.session['username']=username
        request.session['my_freelancer_dic']={'name':name,'email':email,'username':username}
        password = request.POST.get('password')
        selected_skills = request.POST.get('selected_skills')
        if Freelancer.objects.filter(username=username).exists():
            error['error_username'] = 'Username already exists'
            return render(request, 'freelancer/freelancer_signup.html',error)
        if Freelancer.objects.filter(email=email).exists():
            error['error_email'] = 'Email already exists, Try Logging in!'
            return render(request, 'freelancer/freelancer_signup.html',error)

        # Create a new Freelancer object and save it to the database
        freelancer = Freelancer(
            name=name,
            email=email,
            username=username,
            password=password,
            skills=selected_skills
        )
        freelancer.save()
        new_dictionary=freelancer.__dict__
        return render(request,'freelancer/freelancer_homepage.html',{'freelancer': new_dictionary})
    
    return render(request, 'freelancer/freelancer_homepage.html',{'freelancer': freelancer_details})


def upload_profile_freelancer(request):
    freelancer=request.session['my_freelancer_dic']

    if request.method == 'POST':
            if  Photo.objects.filter(username=request.session['username']).exists():
                username=request.session['username']
                freelancer=request.session['my_freelancer_dic']
                photo_update=Photo.objects.get(username=username).update(image=request.FILES['image'])
            freelancer['profile_pic']=photo_update['image']
            return render(request,'freelancer/freelancer_homepage.html',{'freelancer':freelancer})
        username = request.POST.get('username', 'Default Title')  # You can modify as needed
        image = request.FILES.get('image')
        if image:
            Photo.objects.create(username=username, image=image)
            freelancer['profile_pic']=image
            return render(request,'freelancer/freelancer_homepage.html',{'freelancer':freelancer})
    else:
        form = PhotoForm()
    freelancer_details={}
    form = PhotoForm()
    return render(request,'freelancer/freelancer_homepage.html',{'freelancer_details' :freelancer_details,'form':form})

