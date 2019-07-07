from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path( 'logout/' , authapp.logout, name= 'logout' ),
]