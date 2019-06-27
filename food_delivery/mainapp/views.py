from django.shortcuts import render, get_object_or_404
import random
from .models import Product, ProductCategory, ProductCompany


def get_random_restoran():
    restorans = ProductCompany.objects.all()
    # return restorans[0]
    return random.sample(list(restorans), 1)[0]


def get_hot_products():
    restoran = get_random_restoran()
    products = Product.objects.filter(company__name=restoran.name)
    hot_products = random.sample(list(products), 3)[:2]
    return hot_products


def main(request):
    title = 'Главная'
    hot_products = get_hot_products()
    categories=ProductCategory.objects.all()
    content = {'title': title,
               'products': hot_products,
               'categories': categories,
               }
    return render(request, 'mainapp/index.html', content)

def catalog(request):
	categories = ProductCategory.objects.all()

	content = {'categories': categories}
	return render(request, 'mainapp/catalog.html', content)
	#categories = ProductCategory.objects.get(pk=pk)
    
def product (request, pk):
    title = 'product'
    content = {
        'title' : title,
        'links_menu' : ProductCategory.objects.all(),
        'product' : get_object_or_404(Product, pk=pk),
    }
    
    return render(request, 'mainapp/product.html' , content)