from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>)/', basketapp.basket_remove, name='remove'),
    # path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit'),
    path('editt/<int:pk>/', basketapp.editt, name='editt'),
    path('control/<int:pk>/', basketapp.control, name='control'),
    path('delete_all/<int:pk>/', basketapp.delete_all, name='delete_all'),
    path('ret/', basketapp.ret, name='ret'),
    path('order/', basketapp.order, name='order'),
    path('create_order/', basketapp.create_order, name='create_order'),
    path('order_list/', basketapp.order_list, name='order_list'),
    path('order_delete/<int:pk>/', basketapp.order_delete, name='order_delete'),
    path('order_view/<int:pk>/', basketapp.order_view, name='order_view'),
    path('order_pay/<int:pk>/', basketapp.order_pay, name='order_pay'),
]
