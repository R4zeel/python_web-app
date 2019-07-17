from django.shortcuts import render
from django.views.generic.list import ListView
import random
from .models import Products, ProductCategory, Restaurant, RestaurantCategory
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def main(request):
    title = 'Главная'
    categories = ProductCategory.objects.all()
    basket = get_basket(request.user)

    content = {'title': title,
               'categories': categories,
               'basket': basket,
               }
    return render(request, 'mainapp/index.html', content)


def restaurants(request, pk=None):
    if pk == 0:
        restaurant_list = Restaurant.objects.all()
        title = "Все рестораны"
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        restaurant_list = Restaurant.objects.filter(category__pk=pk)
        title = f'Рестораны, доставляющие {category.name}'
    basket = get_basket(request.user)
    content = {
        'title': title,
        'restaurant_list': restaurant_list,
        'basket': basket,
    }
    return render(request, 'mainapp/catalog.html', content)


def products(request, pk):
    links_menu = RestaurantCategory.objects.filter(restaurant=pk)
    restaurant = Restaurant.objects.get(pk=pk)
    products = Products.objects.filter(restaurant=pk)
    title = "Все продукты {}".format(restaurant)
    # else:
    #     category = get_object_or_404(ProductCategory, pk=pk)
    #     products = Products.objects.filter(restaurant__pk=pk)
    #
    #     title = f'Продукты ресторана: {category.name}'
    basket = get_basket(request.user)
    content = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'restaurant': restaurant,
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', content)


def products_list(request, restaurant_pk, category_pk):
    print('Привет', restaurant_pk, category_pk)
    links_menu = RestaurantCategory.objects.filter(restaurant=restaurant_pk)
    restaurant = Restaurant.objects.get(pk=restaurant_pk)
    if category_pk == 0:
        title = 'Все продукты в ресторане {}'.format(restaurant.name)
        products = Products.objects.filter(restaurant=restaurant_pk)
    else:
        category = ProductCategory.objects.get(pk=category_pk)
        products = Products.objects.filter(restaurant=restaurant_pk, category=category_pk)
        title = 'Продукты категории {} в ресторане {}'.format(category.name, restaurant.name)
    basket = get_basket(request.user)
    content = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'restaurant': restaurant,
        'basket': basket,
    }
    return render(request, 'mainapp/products_list.html', content)
