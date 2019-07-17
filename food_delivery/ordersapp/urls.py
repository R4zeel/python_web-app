import ordersapp.views as ordersapp
from django.urls import path

app_name="ordersapp"

urlpatterns = [
	path('create/<int:pk>/', ordersapp.OrderCreate, name='Order_Create')
	path('delete/<int:pk>/', ordersapp.OrderDelete, name='order_delete')
]
