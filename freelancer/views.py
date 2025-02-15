from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request,'user/main_page.html')

def freelancer_signup(request):
    return render(request,'freelancer/freelancer_signup.html')

def client_signup(request):
    return render(request,'client/client_signup.html')

def client_home_page(request):
    return render(request,'client/client_pov.html')

def client_add_project(request):
    return render(request,"client/add_project_client.html")