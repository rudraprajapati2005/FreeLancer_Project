from django.shortcuts import render,HttpResponse
from .models import Freelancer,AboutFreelancer,Project,Client,Users
from .forms import AboutFreelancerForm,FreelancerForm,ProjectForm,ClientForm,UsersForm
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import hashlib
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
        raise ValidationError('Username already exists.')


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least one letter.')

def validate_phone(phone):
    if len(phone) != 10 or not phone.isdigit() or phone[0] not in '6789':
        raise ValidationError('Phone number must be exactly 10 digits and start with 6, 7, 8, or 9.')
  

def client_signup(request):
    user_form = UsersForm()
    client_form = ClientForm()
    
    if request.method == 'POST':
        user_form = UsersForm(request.POST)
        client_form = ClientForm(request.POST)
        
        if user_form.is_valid() and client_form.is_valid():
            # Get data from user form
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            name = user_form.cleaned_data['name']
            phone = user_form.cleaned_data['phone']
            
            # Validate username
            try:
                validate_username(username)
            except ValidationError as e:
                error = {'error_username': ' '.join(e.messages)}
                return render(request, 'client/client_signup.html', {
                    'error': error, 
                    'user_form': user_form,
                    'client_form': client_form
                })

            # Validate password
            try:
                validate_password(password)
            except ValidationError as e:
                error = {'error_password': ' '.join(e.messages)}
                return render(request, 'client/client_signup.html', {
                    'error': error, 
                    'user_form': user_form,
                    'client_form': client_form
                })

            # Validate phone
            try:
                validate_phone(phone)
            except ValidationError as e:
                error = {'error_phone': ' '.join(e.messages)}
                return render(request, 'client/client_signup.html', {
                    'error': error, 
                    'user_form': user_form,
                    'client_form': client_form
                })

            # Check if username already exists in Users model
            if Users.objects.filter(username=username).exists():
                error = {'error_username': 'Username already exists'}
                return render(request, 'client/client_signup.html', {
                    'error': error, 
                    'user_form': user_form,
                    'client_form': client_form
                })

            # Check if email already exists in Users model
            if Users.objects.filter(email=email).exists():
                error = {'error_email': 'Email already exists'}
                return render(request, 'client/client_signup.html', {
                    'error': error, 
                    'user_form': user_form,
                    'client_form': client_form
                })

            # Create user first
            user = user_form.save(commit=False)
            user.password = hash_password(password)
            user.user_type = 'client'
            user.save()

            # Save the client form
            client = client_form.save(commit=False)
            client.user = user
            client.save()

            # Set session data
            request.session['user_type'] = 'client'
            request.session['username'] = username
            request.session['name'] = user.name
            request.session['email'] = user.email
            request.session['phone'] = phone
            request.session['password'] = password 
            # Combine user and client data for the template
            client_dict = model_to_dict(client)
            client_dict.update(model_to_dict(user))
            
            # Redirect to client homepage
            return render(request, 'client/client_homepage.html', {'client': client_dict})
            
    return render(request, 'client/client_signup.html', {
        'user_form': user_form,
        'client_form': client_form
    })

def client_login(request):
    user_type = request.session.get('user_type')
    username = request.session.get('username')
    password = request.session.get('password')

    if user_type == 'client' and username and password:
        try:
            hashed_password = hash_password(password)
            user = Users.objects.get(username=username, password=hashed_password, user_type='client')
            client = Client.objects.get(user=user)
            client_dict = model_to_dict(client)
            client_dict.update(model_to_dict(user))
            # Check if image exists before accessing url
            if client.image and hasattr(client.image, 'url'):
                client_dict['profile_pic'] = client.image.url
            else:
                client_dict['profile_pic'] = None
            settings.USER = client_dict
            return render(request, 'client/client_homepage.html', {'client': client_dict})
        except (Users.DoesNotExist, Client.DoesNotExist):
            pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username:
            try:
                user = Users.objects.get(username=username, user_type='client')
                hashed_password = hash_password(password)
                if user.password == hashed_password:
                    client = Client.objects.get(user=user)
                    request.session['user_type'] = user.user_type
                    request.session['username'] = user.username
                    request.session['name'] = user.name
                    request.session['email'] = user.email
                    request.session['password'] = password
                    client_dict = model_to_dict(client)
                    client_dict.update(model_to_dict(user))
                    # Check if image exists before accessing url
                    if client.image and hasattr(client.image, 'url'):
                        client_dict['profile_pic'] = client.image.url
                    else:
                        client_dict['profile_pic'] = None
                    return render(request, 'client/client_homepage.html', {'client': client_dict})
                else:
                    error = {'error_password': 'Password is incorrect'}
                    return render(request, 'client/client_login.html', {'error': error})
            except Users.DoesNotExist:
                error = {'error_username': 'Username does not exist'}
                return render(request, 'client/client_login.html', {'error': error})
            except Client.DoesNotExist:
                error = {'error_username': 'Invalid client account'}
                return render(request, 'client/client_login.html', {'error': error})
                
    return render(request, 'client/client_login.html')

def client_home_page(request):
    return redirect('client-login-page')
    return render(request,'client/client_homepage.html')

def client_add_project(request):
    return render(request,"client/add_project_client.html")

from django.shortcuts import render, redirect
from .forms import FreelancerForm

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@csrf_protect
def freelancer_signup(request):
    user_form = UsersForm()
    freelancer_form = FreelancerForm()
    
    if request.method == "POST":
        print("THE METHOD IS POST")
        user_form = UsersForm(request.POST)
        freelancer_form = FreelancerForm(request.POST)
        print("Done__1")
        
        # Check if username already exists
        username = request.POST.get('username')
        if Users.objects.filter(username=username).exists():
            error = {'error_username': 'Username already exists'}
            return render(request, 'freelancer/freelancer_signup.html', {
                'error': error,
                'user_form': user_form,
                'freelancer_form': freelancer_form
            })

        # Check if email already exists
        email = request.POST.get('email')
        if Users.objects.filter(email=email).exists():
            error = {'error_email': 'Email already exists'}
            return render(request, 'freelancer/freelancer_signup.html', {
                'error': error,
                'user_form': user_form,
                'freelancer_form': freelancer_form
            })

        if user_form.is_valid():
            try:
                print("is_valid")
                # Get data from user form
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']
                email = user_form.cleaned_data['email']
                name = user_form.cleaned_data['name']
                phone = user_form.cleaned_data['phone']
                selected_skills = request.POST.get('selected_skills')
                
                print(f"Received form data - Username: {username}, Email: {email}, Skills: {selected_skills}")
                
                # Validate username
                try:
                    validate_username(username)
                except ValidationError as e:
                    error = {'error_username': ' '.join(e.messages)}
                    return render(request, 'freelancer/freelancer_signup.html', {
                        'error': error, 
                        'user_form': user_form,
                        'freelancer_form': freelancer_form
                    })

                # Validate password
                try:
                    validate_password(password)
                except ValidationError as e:
                    error = {'error_password': ' '.join(e.messages)}
                    return render(request, 'freelancer/freelancer_signup.html', {
                        'error': error, 
                        'user_form': user_form,
                        'freelancer_form': freelancer_form
                    })

                # Validate phone
                try:
                    validate_phone(phone)
                except ValidationError as e:
                    error = {'error_phone': ' '.join(e.messages)}
                    return render(request, 'freelancer/freelancer_signup.html', {
                        'error': error, 
                        'user_form': user_form,
                        'freelancer_form': freelancer_form
                    })

                # Create user first
                user = user_form.save(commit=False)
                user.password = hash_password(password)
                user.user_type = 'freelancer'
                user.save()
                print(f"User created successfully: {user.username}")

                # Create freelancer profile
                freelancer = Freelancer.objects.create(
                    user=user,
                    skills=selected_skills or ''  # Use empty string if no skills selected
                )
                print(f"Freelancer profile created successfully: {freelancer.user.username}")

                # Create about freelancer profile
                about_freelancer = AboutFreelancer.objects.create(
                    username=username,
                    freelancer=freelancer
                )
                print(f"About freelancer profile created successfully: {about_freelancer.username}")

                # Set session data
                request.session['freelancer'] = username
                request.session['username'] = username
                request.session['name'] = user.name
                request.session['email'] = user.email
                request.session['phone'] = phone
                request.session['my_freelancer_dic'] = model_to_dict(freelancer)

                messages.success(request, 'Account created successfully!')
                return redirect('freelancer-home')

            except Exception as e:
                print(f"Error during signup: {str(e)}")
                messages.error(request, f'An error occurred during signup: {str(e)}')
                return render(request, 'freelancer/freelancer_signup.html', {
                    'user_form': user_form,
                    'freelancer_form': freelancer_form,
                    'error': {'error_general': f'An error occurred: {str(e)}'}
                })
        else:
            print("Form validation failed:")
            print("User form errors:", user_form.errors)
            error = {}
            if user_form.errors:
                for field, errors in user_form.errors.items():
                    error[f'error_{field}'] = errors[0]
            return render(request, 'freelancer/freelancer_signup.html', {
                'user_form': user_form,
                'freelancer_form': freelancer_form,
                'error': error
            })

    return render(request, 'freelancer/freelancer_signup.html', {
        'user_form': user_form,
        'freelancer_form': freelancer_form
    })

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
                freelancer=freelancer
            )
            about_freelancer.save()

            # Set session data
            request.session['freelancer'] = username
            request.session['username'] = username
            request.session['my_freelancer_dic'] = model_to_dict(freelancer)

            # Redirect to freelancer home page
            return redirect('freelancer-home')

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
                # Get the user object first
                user = Users.objects.get(username=username, user_type='freelancer')
                
                # Get the freelancer object through user relationship
                freelancer = Freelancer.objects.get(user=user)
                
                # Try to get existing AboutFreelancer
                about_freelancer = AboutFreelancer.objects.get(username=username)
                about_freelancer.image = image
                about_freelancer.save()
                print('AboutFreelancer updated')
            except AboutFreelancer.DoesNotExist:
                # Create new AboutFreelancer if doesn't exist
                about_freelancer = AboutFreelancer.objects.create(
                    username=username,
                    freelancer=freelancer
                )
                about_freelancer.image = image
                about_freelancer.save()
                print('AboutFreelancer created')
            
            # Combine all the data
            freelancer_data = model_to_dict(freelancer)
            about_data = model_to_dict(about_freelancer, exclude=['image'])
            
            # Add user data
            freelancer_data.update({
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'phone': user.phone
            })
            
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
        # Get the user object first
        user = Users.objects.get(username=username, user_type='freelancer')
        
        # Get the freelancer object through user relationship
        freelancer = Freelancer.objects.get(user=user)
        freelancer_data = model_to_dict(freelancer)
        
        # Add user data
        freelancer_data.update({
            'name': user.name,
            'email': user.email,
            'username': user.username,
            'phone': user.phone
        })
        
        try:
            about_freelancer = AboutFreelancer.objects.get(username=username)
            about_data = model_to_dict(about_freelancer, exclude=['image'])
            if about_freelancer.image:
                about_data['profile_pic'] = about_freelancer.image.url
            freelancer_data.update(about_data)
        except AboutFreelancer.DoesNotExist:
            pass
        
        return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer_data})
    except (Users.DoesNotExist, Freelancer.DoesNotExist):
        return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': {'username': username}})

from django.forms.models import model_to_dict

@csrf_protect
def freelancer_login(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username_email')
            password = request.POST.get('password')

            if not username or not password:
                return render(request, "freelancer/freelancer_login.html", {
                    'error_username': 'Please provide both username and password.'
                })

            # Hash the provided password
            hashed_password = hash_password(password)

            # Check if user exists and is a freelancer
            try:
                user = Users.objects.get(username=username, user_type='freelancer')
            except Users.DoesNotExist:
                return render(request, "freelancer/freelancer_login.html", {
                    'error_username': 'Username does not exist or is not a freelancer.'
                })
            
            # Verify password using hashed password
            if user.password != hashed_password:
                return render(request, "freelancer/freelancer_login.html", {
                    'error_password': 'Incorrect password.'
                })

            # Get freelancer profile
            try:
                freelancer = Freelancer.objects.get(user=user)
            except Freelancer.DoesNotExist:
                return render(request, "freelancer/freelancer_login.html", {
                    'error_username': 'Freelancer profile not found.'
                })

            # Create base freelancer dictionary with user data
            freelancer_dict = model_to_dict(freelancer)
            freelancer_dict.update({
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'phone': user.phone
            })

            # Get about freelancer data
            try:
                about_freelancer = AboutFreelancer.objects.get(username=user.username)
                about_data = model_to_dict(about_freelancer, exclude=['image'])
                
                # Add profile picture if exists
                if about_freelancer.image:
                    about_data['profile_pic'] = about_freelancer.image.url
                
                # Update freelancer dictionary with about data
                freelancer_dict.update(about_data)
                
            except AboutFreelancer.DoesNotExist:
                # Create new AboutFreelancer if doesn't exist
                about_freelancer = AboutFreelancer.objects.create(
                    username=username,
                    freelancer=freelancer
                )
                freelancer_dict['profile_pic'] = None
                freelancer_dict['about_freelancer'] = None
                freelancer_dict['gitLinks'] = None
                freelancer_dict['links'] = None
                freelancer_dict['experience'] = None

            # Set session data
            request.session['freelancer'] = user.username
            request.session['username'] = user.username
            request.session['name'] = user.name
            request.session['email'] = user.email
            request.session['phone'] = user.phone
            request.session['my_freelancer_dic'] = freelancer_dict

            messages.success(request, 'Login successful!')
            return render(request, "freelancer/freelancer_homepage.html", {'freelancer': freelancer_dict})

        except Exception as e:
            print(f"Login error: {str(e)}")
            return render(request, "freelancer/freelancer_login.html", {
                'error_username': 'An error occurred. Please try again.'
            })

    return render(request, "freelancer/freelancer_login.html")

def freelancer_logout(request):
    # Clear all session data
    request.session.flush()
    
    # Clear specific session variables
    request.session['freelancer'] = ''
    request.session['username'] = ''
    request.session['my_freelancer_dic'] = ''
    request.session['user_type'] = ''
    
    # Add a success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to home page
    return redirect('home')

from django.http import HttpResponseRedirect
from django.urls import reverse

def save_description(request):
    if request.method == 'POST':
        username = request.session.get('username')
        field_type = request.POST.get('field_type')
        description = request.POST.get('description')
        
        try:
            user = Users.objects.get(username=username, user_type='freelancer')
            freelancer = Freelancer.objects.get(user=user)
            
            if field_type == 'skills':
                # Update freelancer skills directly
                freelancer.skills = description
                freelancer.save()
                
                # Get about_freelancer data
                about_freelancer = AboutFreelancer.objects.filter(username=username).first()
                if about_freelancer:
                    about_freelancer_dict = model_to_dict(about_freelancer, exclude=['image'])
                    if about_freelancer.image and hasattr(about_freelancer.image, 'url'):
                        about_freelancer_dict['profile_pic'] = about_freelancer.image.url
                    
                    # Combine freelancer and about_freelancer data
                    freelancer_data = model_to_dict(freelancer)
                    about_freelancer_dict.update(freelancer_data)
                    return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': about_freelancer_dict})
            else:
                # Handle other fields (about, git, links)
                about_freelancer = AboutFreelancer.objects.filter(username=username).first()
                if about_freelancer:
                    if field_type == 'about':
                        about_freelancer.about_freelancer = description
                    elif field_type == 'git':
                        about_freelancer.gitLinks = description
                    elif field_type == 'links':
                        about_freelancer.links = description
                    
                    about_freelancer.save()
                    
                    about_freelancer_dict = model_to_dict(about_freelancer, exclude=['image'])
                    if about_freelancer.image and hasattr(about_freelancer.image, 'url'):
                        about_freelancer_dict['profile_pic'] = about_freelancer.image.url
                    
                    freelancer_data = model_to_dict(freelancer)
                    about_freelancer_dict.update(freelancer_data)
                    
                    return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': about_freelancer_dict})
            
            return render(request, "freelancer/freelancer_homepage.html", {'freelancer': {'username': username}})
            
        except (Users.DoesNotExist, Freelancer.DoesNotExist):
            return redirect('freelancer-login-page')

    return HttpResponse("OOPS! Something went wrong.")
def create_project(request):
    if request.method == 'POST':
        try:
            username = request.session.get('username')
            user = Users.objects.get(username=username, user_type='client')
            client = Client.objects.get(user=user)
            client_dict = model_to_dict(client)
            client_dict.update(model_to_dict(user))
            
            if client.image:
                client_dict['profile_pic'] = client.image.url
            
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                project.posted_by = client
                project.save()
                messages.success(request, 'Project created successfully!')
                return render(request, 'client/client_homepage.html', {'client': client_dict})
            else:
                messages.error(request, 'Please correct the errors below.')
                return render(request, 'client/create_project.html', {'form': form})
                
        except (Users.DoesNotExist, Client.DoesNotExist):
            messages.error(request, 'You must be logged in as a client to create projects.')
            return redirect('client-login-page')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'client/create_project.html', {'form': form})
    else:
        username = request.session.get('username')
        try:
            user = Users.objects.get(username=username, user_type='client')
            client = Client.objects.get(user=user)
            client_dict = model_to_dict(client)
            client_dict.update(model_to_dict(user))
            if client.image:
                client_dict['profile_pic'] = client.image.url
            form = ProjectForm()
            return render(request, 'client/create_project.html', {
                'form': form,
                'client': client_dict  # Pass client data for cancel button
            })
        except (Users.DoesNotExist, Client.DoesNotExist):
            return redirect('client-login-page')

def user_type(request):
    return render(request, 'user/user_type.html')

def browse_projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'user/Browse_projects.html', {'projects': projects})

def view_freelancers(request):
    freelancers = Freelancer.objects.all()
    
    for fr in freelancers:
        fr.skills = fr.skills.replace('_', ' ')
        if AboutFreelancer.objects.filter(username=fr.username):
            user_freelancer=AboutFreelancer.objects.get(username=fr.username)
            fr.profile_pic=user_freelancer.image.url
        
    return render(request, 'user/Freelancers.html', {'freelancers': freelancers})

def freelancer_home(request):
    username = request.session.get('username')
    if not username:
        return redirect('freelancer-login-page')
    
    try:
        # Get the user object first
        user = Users.objects.get(username=username, user_type='freelancer')
        
        # Get the freelancer profile
        freelancer = Freelancer.objects.get(user=user)
        freelancer_data = model_to_dict(freelancer)
        
        # Add user data to freelancer data
        freelancer_data.update({
            'name': user.name,
            'email': user.email,
            'username': user.username,
            'phone': user.phone
        })
        
        # Try to get about freelancer data
        try:
            about_freelancer = AboutFreelancer.objects.get(username=username)
            about_data = model_to_dict(about_freelancer, exclude=['image'])
            
            # Add profile picture if exists
            if about_freelancer.image:
                about_data['profile_pic'] = about_freelancer.image.url
            
            # Update freelancer data with about data
            freelancer_data.update(about_data)
            
        except AboutFreelancer.DoesNotExist:
            # If no about data exists, create it
            about_freelancer = AboutFreelancer.objects.create(
                username=username,
                freelancer=freelancer
            )
            freelancer_data['profile_pic'] = None
        
        # Update session data
        request.session['my_freelancer_dic'] = freelancer_data
        
        return render(request, 'freelancer/freelancer_homepage.html', {'freelancer': freelancer_data})
        
    except Users.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('freelancer-login-page')
    except Freelancer.DoesNotExist:
        messages.error(request, 'Freelancer profile not found.')
        return redirect('freelancer-login-page')
    except Exception as e:
        print(f"Error in freelancer_home: {str(e)}")
        messages.error(request, 'An error occurred while loading your profile.')
        return redirect('freelancer-login-page')

def client_logout(request):
    # Clear all session data
    request.session.flush()
    
    # Clear specific session variables
    request.session['user_type'] = ''
    request.session['username'] = ''
    request.session['name'] = ''
    request.session['email'] = ''
    request.session['phone'] = ''
    
    # Add a success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to home page
    return redirect('home')

def save_client_details(request):
    if request.method == 'POST':
        username = request.session.get('username')
        field_type = request.POST.get('field_type')
        updated_value = request.POST.get('description')
        
        try:
            user = Users.objects.get(username=username, user_type='client')
            client = Client.objects.get(user=user)
            
            if field_type == 'company':
                client.companyname = updated_value
            elif field_type == 'address':
                client.address = updated_value
            elif field_type == 'business_email':
                client.businessEmail = updated_value
                
            client.save()
            
            client_dict = model_to_dict(client)
            client_dict.update({
                'name': user.name,
                'email': user.email,
                'username': user.username,
                'phone': user.phone
            })
            
            return render(request, 'client/client_homepage.html', {'client': client_dict})
            
        except (Users.DoesNotExist, Client.DoesNotExist):
            return redirect('client-login-page')

    return HttpResponse("Something went wrong.")

def upload_profile_client(request):
    username = request.session.get('username')
    
    if request.method == 'POST':
        if 'image' in request.FILES:
            if not username:
                return redirect('client-login-page')
                
            image = request.FILES.get('image')
            
            try:
                user = Users.objects.get(username=username, user_type='client')
                client = Client.objects.get(user=user)
                
                client.image = image
                client.save()
                
                client_dict = model_to_dict(client)
                client_dict.update({
                    'name': user.name,
                    'email': user.email,
                    'username': user.username,
                    'phone': user.phone
                })
                
                if client.image:
                    client_dict['profile_pic'] = client.image.url
                
                return render(request, 'client/client_homepage.html', {'client': client_dict})
                
            except (Users.DoesNotExist, Client.DoesNotExist):
                return redirect('client-login-page')
    
    return redirect('client-home-page')

def client_my_projects(request):
    try:
        username = request.session.get('username')
        user = Users.objects.get(username=username, user_type='client')
        client = Client.objects.get(user=user)
        projects = Project.objects.filter(posted_by=client).order_by('-created_at')
        
        client_dict = model_to_dict(client)
        client_dict.update(model_to_dict(user))
        if client.image:
            client_dict['profile_pic'] = client.image.url
            
        context = {
            'client': client_dict,
            'projects': projects
        }
        return render(request, 'client/client_myprojects.html', context)
    except (Users.DoesNotExist, Client.DoesNotExist):
        return redirect('client-login-page')

def project_card(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project_dict=model_to_dict(project)
    skill = [s.replace('_', ' ') for s in project.skills_required.split(",")]
    project_dict['skills']=skill
    client_info_model=project.posted_by
    client_info_dict=model_to_dict(client_info_model)
    client_user_info=model_to_dict(client_info_model.user)
    project_dict.update(client_user_info)
    project_dict.update(client_info_dict)
    print(project_dict)
    return render(request,"user/Project_information.html",
                   {'project' : project_dict})


def profile(request):
    return render(request, "client/client_homepage.html", { 'client' : request.session  })