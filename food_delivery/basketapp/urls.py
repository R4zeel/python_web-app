from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>)/', basketapp.basket_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit'),
    path('control/<int:pk>/', basketapp.control, name='control'),
    path('delete_all/<int:pk>/', basketapp.delete_all, name='delete_all'),
    path('ret/', basketapp.ret, name='ret')
]