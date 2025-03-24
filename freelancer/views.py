from django.shortcuts import render,HttpResponse
from .models import Freelancer,AboutFreelancer,Project,Client,Users
from .forms import AboutFreelancerForm,FreelancerForm,ProjectForm,ClientForm
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
    if Users.objects.filter(username=username).exists():
        raise ValidationError('Username already exists with given data try again.')


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
    user_type = request.session.get('user_type')
    username = request.session.get('username')
    password = request.session.get('password')

    if user_type is None and username and password:
        if Users.objects.filter(username=username, password=password).exists():
            user = Users.objects.get(username=username)
            client = model_to_dict(Client.objects.get(username=username))
            return render(request, 'user/Home.html', {'client': client})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username:
            if Users.objects.filter(username=username).exists():
                user = Users.objects.get(username=username)
                if user.password == password:
                    request.session['user_type'] = user.user_type
                    request.session['username'] = user.username
                    request.session['name'] = user.name
                    request.session['email'] = user.email
            
                    client = model_to_dict(Client.objects.get(username=username))
                    return render(request, 'user/Home.html', {'client': client})
                else:
                    error = {'error_password': 'Password is incorrect'}
                    return render(request, 'client/client_login.html', {'error': error})
            else:
                error = {'error_username': 'Username does not exist'}
                return render(request, 'client/client_login.html', {'error': error})
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

            return redirect('')  # Redirect to a success page
    else:
        form = FreelancerForm()
    return render(request, 'freelancer/freelancer_signup.html', {'form': form})

def show_details_freelancer(request):
    error = {}
    freelancer_details = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_skills = request.POST.get('selected_skills')

        # Store session data
        request.session['name'] = name
        request.session['email'] = email
        request.session['username'] = username
        request.session['my_freelancer_dic'] = {'name': name, 'email': email, 'username': username}

        # Check if username or email already exists
        if Freelancer.objects.filter(username=username).exists():
            error['error_username'] = 'Username already exists'
            return render(request, 'freelancer/freelancer_signup.html', error)
        if Freelancer.objects.filter(email=email).exists():
            error['error_email'] = 'Email already exists, Try Logging in!'
            return render(request, 'freelancer/freelancer_signup.html', error)

        try:
            # First create and save the Freelancer object
            freelancer = Freelancer(
                name=name,
                email=email,
                username=username,
                password=password,
                skills=selected_skills
            )
            freelancer.save()

            # Then create and save the AboutFreelancer object
            about_freelancer = AboutFreelancer(
                username=username,
                freelancer=freelancer  # Now freelancer has an ID and can be referenced
            )
            about_freelancer.save()

            # Combine the data for the template
            freelancer_data = model_to_dict(freelancer)
            about_data = model_to_dict(about_freelancer)
            freelancer_data.update(about_data)

            return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer_data})
        except Exception as e:
            error['error_general'] = str(e)
            return render(request, 'freelancer/freelancer_signup.html', error)

    return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer_details})



def upload_profile_freelancer(request):
    username = request.session.get('username')
    
    if request.method == 'POST':
        if 'image' in request.FILES:
            if not username:
                return redirect('freelancer-login-page')
                
            image = request.FILES.get('image')
            
            try:
                # Get the freelancer object
                freelancer = Freelancer.objects.get(username=username)
                
                # Try to get existing AboutFreelancer
                about_freelancer = AboutFreelancer.objects.get(username=username)
                about_freelancer.image = image
                about_freelancer.save()
                print('AboutFreelancer updated')
            except AboutFreelancer.DoesNotExist:
                # Create new AboutFreelancer if doesn't exist
                about_freelancer = AboutFreelancer(username=username, image=image, freelancer=freelancer)
                about_freelancer.save()
                print('AboutFreelancer created')
            
            # Combine all the data
            freelancer_data = model_to_dict(freelancer)
            about_data = model_to_dict(about_freelancer, exclude=['image'])
            
            # Add the profile picture URL
            if about_freelancer.image:
                about_data['profile_pic'] = about_freelancer.image.url
            
            # Combine the data, ensuring freelancer data takes precedence
            about_data.update(freelancer_data)
            
            # Update session data
            request.session['my_freelancer_dic'] = about_data
            
            return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': about_data})

    # Handle GET request
    try:
        freelancer = Freelancer.objects.get(username=username)
        freelancer_data = model_to_dict(freelancer)
        
        try:
            about_freelancer = AboutFreelancer.objects.get(username=username)
            about_data = model_to_dict(about_freelancer, exclude=['image'])
            if about_freelancer.image:
                about_data['profile_pic'] = about_freelancer.image.url
            freelancer_data.update(about_data)
        except AboutFreelancer.DoesNotExist:
            pass
        
        return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer_data})
    except Freelancer.DoesNotExist:
        return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': {'username': username}})

from django.forms.models import model_to_dict

def freelancer_login(request):
    if request.method == "POST":
        username = request.POST.get('username_email')
        password = request.POST.get('password')
        if Freelancer.objects.filter(username=username).exists():
            freelancer = Freelancer.objects.get(username=username)
            if freelancer.password == password:
                request.session['freelancer'] = freelancer.username
                request.session['username'] = freelancer.username 
                request.session['my_freelancer_dic'] = model_to_dict(freelancer)
                about_freelancer = AboutFreelancer.objects.filter(username=freelancer.username).first()
                freelancer_dict = model_to_dict(freelancer)
                freelancer_dict.update(model_to_dict(about_freelancer, exclude=['image']))
                if about_freelancer:
                    freelancer_dict['profile_pic'] = about_freelancer.image.url
                return render(request, "freelancer/freelancer_homepage.html", {'freelancer': freelancer_dict})
            else:
                error = {'error_password': 'Password is incorrect'}
                return render(request, "freelancer/freelancer_login.html", error)
        else:
            error = {'error_username': 'Username does not exist'}
            return render(request, "freelancer/freelancer_login.html", error)
    
    # if request.session['username']:
    #     freelancer = Freelancer.objects.get(username=request.session['username'])
    #     freelancer_dict = model_to_dict(freelancer)
    #     about_freelancer=AboutFreelancer.objects.get(username=freelancer.username)
    #     freelancer_dict.update(model_to_dict(about_freelancer))
    #     freelancer_dict['profile_pic']=about_freelancer.image.url
    #     return render(request, "freelancer/freelancer_homepage.html", {'freelancer': freelancer_dict})
    else :
        return render(request, "freelancer/freelancer_login.html")

from django.http import HttpResponseRedirect
from django.urls import reverse

def save_description(request):
    if request.method == 'POST':
        username = request.session.get('username')
        field_type = request.POST.get('field_type')
        description = request.POST.get('description')
        
        about_freelancer = AboutFreelancer.objects.filter(username=username).first()
        if about_freelancer:
            # Update the appropriate field based on field_type
            if field_type == 'about':
                about_freelancer.about_freelancer = description
            elif field_type == 'git':
                about_freelancer.gitLinks = description
            elif field_type == 'links':
                about_freelancer.links = description
            
            about_freelancer.save()
            
            # Create the response data, explicitly excluding the image field
            about_freelancer_dict = model_to_dict(about_freelancer, exclude=['image'])
            
            # Only add image URL if image exists and has a file associated
            if about_freelancer.image and hasattr(about_freelancer.image, 'url'):
                about_freelancer_dict['profile_pic'] = about_freelancer.image.url
            
            # Add freelancer data if it exists
            if about_freelancer.freelancer:
                freelancer_data = model_to_dict(about_freelancer.freelancer)
                
                about_freelancer_dict.update(freelancer_data)
                print("DONE")
            about_freelancer_dict['profile_pic'] = about_freelancer.image.url
            
            return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': about_freelancer_dict})
        return render(request, "freelancer/freelancer_homepage.html", {'freelancer': {'username': username}})

    return HttpResponse("OOPS! Something went wrong.")
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