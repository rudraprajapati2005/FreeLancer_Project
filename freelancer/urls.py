from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home, name='home'),
    path("freelancer-signup",views.freelancer_signup,name='freelancer-signup-page'),
    path("details",views.show_details_freelancer,name='freelancer-details-page'),
    path("client-signup",views.client_signup,name='client-signup-page'),
    path("client-login",views.client_login,name='client-login-page'),
    path("client-home",views.client_home_page,name='client-home-page'),
    path("client-home/add-project",views.client_add_project,name='client-add-project'),
    path("upload-profile-freelancer",views.upload_profile_freelancer,name='upload-profile-freelancer'),
    path("freelancer-login",views.freelancer_login,name='freelancer-login-page'),
    path("user-type", views.user_type, name='user_type'),
    path("browse_projects", views.browse_projects, name="browse_projects"),
    path("client/create_project", views.create_project, name="client-create-project"),
    path("Freelancers", views.view_freelancers, name="view_freelancers"),
]