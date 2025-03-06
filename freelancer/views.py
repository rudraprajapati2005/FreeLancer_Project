from django.shortcuts import render,HttpResponse
from .models import Freelancer,Photo,Project,Client,Users
from .forms import PhotoForm,FreelancerForm,ProjectForm,ClientForm
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your views here.
def home(request):
        request.session['freelancer']=''
        return render(request, "user/Home.html")


# def freelancer_signup(request):
#     return render(request,'freelancer/freelancer_signup.html')
def validate_username(username):
    if not all(char.isalnum() or char == '_' for char in username):
        raise ValidationError('Username can only contain letters, digits, and underscores.')

def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')

def validate_phone(phone):
    if len(phone) != 10 or not phone.isdigit() or phone[0] not in '6789':
        raise ValidationError('Phone number must be exactly 10 digits and start with 6, 7, 8, or 9.')
  

def client_signup(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        
        # Validate username
        try:
            validate_username(username)
        except ValidationError as e:
            error = {'error_username': ' '.join(e.messages)}
            return render(request, 'client/client_signup.html', {'error': error, 'form': form})

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            error = {'error_password': ' '.join(e.messages)}
            return render(request, 'client/client_signup.html', {'error': error, 'form': form})

        # Validate phone
        try:
            validate_phone(phone)
        except ValidationError as e:
            error = {'error_phone': ' '.join(e.messages)}
            return render(request, 'client/client_signup.html', {'error': error, 'form': form})

        # Check if username already exists
        if Users.objects.filter(username=username).exists():
            error = {'error_username': 'Username already exists'}
            return render(request, 'client/client_signup.html', {'error': error, 'form': form})

        # Check if business email does not exist
        if not Users.objects.filter(email=request.POST.get('businessEmail')).exists():
            userForm = Users(
                name=request.POST.get('name'),
                email=request.POST.get('businessEmail'),
                username=username,
                password=password,
                user_type='client'
            )
            userForm.save()
        else:
            error = {'error_email': 'Business email already exists'}
            return render(request, 'client/client_signup.html', {'error': error, 'form': form})

        # Save the client form
        if form.is_valid():
            form.save()
            request.session['user_type'] = 'client'
            request.session['username'] = username
            request.session['name'] = request.POST.get('name')
            request.session['email'] = request.POST.get('businessEmail')
            request.session['phone'] = phone
            request.session['password']=password
            client=model_to_dict(Client.objects.get(username=username))
            return render(request, 'user/Home.html', {'client': client})
    return render(request, 'client/client_signup.html', {'form': form})

def client_login(request):
    print(request.session.get('user_type'))
    if not request.session.get('user_type'):
        if Users.objects.filter(username=request.session['username'],password=request.session['password']).exists():
            user = Users.objects.get(username=request.session['username'])
            client=model_to_dict(Client.objects.get(username=request.session['username']))
            return render(request, 'user/Home.html',{'client':client} )
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Users.objects.filter(username=username).exists():
            user = Users.objects.get(username=username)
            if user.password == password:
                request.session['user_type'] = user.user_type
                request.session['username'] = user.username
                request.session['name'] = user.name
                request.session['email'] = user.email
                client=model_to_dict(Client.objects.get(username=username))
                return render(request, 'user/Home.html', {'client': client})
            else:
                error = {'error_password': 'Password is incorrect'}
                return render(request, 'client/client_login.html', {'error':error})
        else:
            error = {'error_username': 'Username does not exist'}
            return render(request, 'client/client_login.html', {'error':error})
    return render(request, 'client/client_login.html')
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
    
    freelancer = request.session.get('my_freelancer_dic', {})
    print('here'+str(freelancer))
    if request.method == 'POST':
        if 'image' in request.FILES:
            username = request.session.get('username')
            if not username:
                return redirect('freelancer-login-page')
                
            image = request.FILES.get('image')
            
            try:
                # Try to get existing photo
                photo = Photo.objects.get(username=username)
                photo.image = image
                photo.save()
                print('Photo updated')
            except Photo.DoesNotExist:
                # Create new photo if doesn't exist
                photo = Photo(username=username, image=image)
                photo.save()
                print('Photo created')
            # Update session data
            print('nothing happened')
            freelancer['profile_pic'] = photo.image.url
            request.session['my_freelancer_dic'] = freelancer
            
            return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer})

    # Handle GET request
    if freelancer:
        try:
            photo = Photo.objects.get(username=request.session.get('username'))
            freelancer['profile_pic'] = photo.image.url
        except Photo.DoesNotExist:
            pass

    form = PhotoForm()
    return render(request, 'freelancer/freelancer_homepage.html', 
                  {'freelancer': freelancer, 'form': form})

def freelancer_login(request):
    if(request.method=="POST"):
        username=request.POST.get('username_email')
        password=request.POST.get('password')
        if Freelancer.objects.filter(username=username).exists():
            freelancer=Freelancer.objects.get(username=username)
            if(freelancer.password==password):
                request.session['freelancer']=freelancer.username
                request.session['username']=freelancer.username 
                request.session['my_freelancer_dic']=model_to_dict(freelancer)
                if Photo.objects.filter(username=freelancer.username).exists():
                    photo=Photo.objects.get(username=freelancer.username)
                    freelancer=model_to_dict(freelancer)
                    freelancer['profile_pic']=photo.image.url
                return render(request,"freelancer/freelancer_homepage.html",{'freelancer':freelancer})
            else:
                error={'error_password':'Password is incorrect'}
                return render(request,"freelancer/freelancer_login.html",error)
        else:
            error={'error_username':'Username does not exist'}
            return render(request,"freelancer/freelancer_login.html",error)
    return render(request,"freelancer/freelancer_login.html")


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Successfully Saved')  # Redirect to a view that lists the projects
    else:
        form = ProjectForm()
    
    return render(request, 'client/create_project.html', {'form': form})

def user_type(request):
    return render(request, 'user/user_type.html')

def browse_projects(request):
    return render(request, 'user/Browse_projects.html')


def view_freelancers(request):
    return render(request, 'user/Freelancers.html')