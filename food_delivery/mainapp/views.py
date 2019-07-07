from django.shortcuts import render
from django.views.generic.list import ListView
import random
from .models import Products, ProductCategory, ProductCompany
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest


def get_random_restoran():
    restorans = ProductCompany.objects.all()
    # return restorans[0]
    return random.sample(list(restorans), 1)[0]


def get_hot_products():
    restoran = get_random_restoran()
    products = Products.objects.filter(company__name=restoran.name)
    hot_products = random.sample(list(products), 2)[:2]
    return hot_products


def main(request):
    title = 'Главная'
    hot_product = get_hot_products()
    categories = ProductCategory.objects.all()
    content = {'title': title,
               'products': hot_product,
               'categories': categories,
               }
    return render(request, 'mainapp/index.html', content)


class CompanyCatalogView(ListView):
    model = ProductCompany
    template_name = 'mainapp/catalog.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


def restoran_of_category(request, pk=None):
    # links_menu = ProductCategory.objects.filter(is_active=True)

    # basket = get_basket(request.user)

    if pk != None:
        if pk == 0:
            restorans = ProductCompany.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=int(pk))
            products = Products.objects.filter(category__pk=int(pk))
            restorans = []
            for product in products:
                if ProductCompany.objects.get(name=product.company) in restorans:
                    continue
                else:
                    restorans.append(ProductCompany.objects.get(name=product.company))
    title = 'Рестораны с категорией {}'.format(category.name)

    content = {
        'title': title,
        'category': category,
        'restorans': restorans,

    }

    return render(request, 'mainapp/restorans_list.html', content)


def products_restoran(request, pk=None):
    if pk != None and pk != 0:
        restoran = get_object_or_404(ProductCompany, pk=pk)
        # print(restoran.name)
        products = Products.objects.filter(company__name=restoran.name)


        title = 'Продукты ресторана: {}'.format(restoran.name)

        content = {
            'title': title,
            'restoran': restoran,
            'products': products,

            }

        return render(request, 'mainapp/products_restoran.html', content)
    else:
        return