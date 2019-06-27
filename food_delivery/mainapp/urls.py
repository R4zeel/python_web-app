from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns =[
    path('product/<int:pk>/', mainapp.product, name='product')
]