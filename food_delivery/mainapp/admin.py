from django.contrib import admin
from .models import ProductCategory, Products, Restaurant, RestaurantCategory

admin.site.register(ProductCategory)
admin.site.register(Products)
admin.site.register(Restaurant)
admin.site.register(RestaurantCategory)