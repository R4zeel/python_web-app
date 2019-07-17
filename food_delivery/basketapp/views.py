from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Products
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('catalog:products_list', args=[product.restaurant__pk, product.category__pk]))
    basket = Basket.objects.filter(user=request.user, product=product).first()
    basket_user = Basket.objects.filter(user=request.user)
    restauran = product.restaurant
    if not basket:
        if not basket_user or product.restaurant == basket_user[0].restauran:
            basket = Basket(user=request.user, product=product, restauran=restauran)
        else:
            return HttpResponseRedirect(reverse('basket:control', args=[product.pk]))

    basket.quantity += 1
    basket.save()

    # return HttpResponseRedirect('http://127.0.0.1:8000/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)

    # if request.method == 'POST':
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {'basket_items': basket_items}
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})

@login_required
def control(request, pk):
    basket = Basket.objects.filter(user=request.user).first()
    print('Привет', basket)
    product = Products.objects.get(pk=pk)
    content = {'product': product, 'basket': basket}
    return render(request, 'basketapp/control.html', content)


@login_required
def delete_all(request, pk):
    basket = Basket.objects.filter(user=request.user)
    print(basket)
    basket.delete()
    product = Products.objects.get(pk=pk)
    print('Привет', product.restaurant.pk, product.category.pk)
    return HttpResponseRedirect(reverse('catalog:products_list', args=[product.restaurant.pk, product.category.pk]))


@login_required
def ret(request):
    product = Basket.objects.filter(user=request.user).first()
    return HttpResponseRedirect(reverse('catalog:products_list', args=[product.restauran.pk, 0]))
