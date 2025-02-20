from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [

    path("",views.home),
    path("freelancer-signup",views.freelancer_signup,name='freelancer-signup-page'),
    path("details",views.show_details_freelancer,name='freelancer-details-page'),
    path("client-signup",views.client_signup,name='client-signup-page'),
    path("client-home",views.client_home_page,name='client-home-page'),
    path("client-home/add-project",views.client_add_project,name='client-add-project'),
    path("upload-profile-freelancer",views.upload_profile_freelancer,name='upload-profile-freelancer')
]