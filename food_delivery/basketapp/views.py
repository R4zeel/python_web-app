from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Products
from django.contrib.auth.decorators import login_required
from django.urls import reverse


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
    user_basket = Basket.objects.filter(user=request.user)
    if user_basket[-1].product.company == product.company or len(user_basket) == 0:
        basket = Basket.objects.filter(user=request.user, product=product).first()

        if not basket:
            basket = Basket(user=request.user, product=product)

        basket.quantity += 1
        basket.save()

        # return HttpResponseRedirect('http://127.0.0.1:8000/')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect('http://127.0.0.1:8000/category/')

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)

    if request.method == 'POST':
        basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
