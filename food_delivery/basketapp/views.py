from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket, Order, OrderItems
from mainapp.models import Products
from basketapp.forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


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


@login_required
def editt(request, pk):
    if str(pk) in request.POST:
        quantity = request.POST.get(str(pk))
        # print('Привет', quantity)
        item = Basket.objects.get(pk=pk)
        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def order(request):
    title = 'Оформление заказа'
    if request.method == 'POST':
        print('Привет')
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:

        order_form = OrderForm()
        user = request.user
        print(type(order_form))
    return render(request, 'basketapp/create_order.html', {'title': title, 'order_form': order_form, 'user': user})


def create_order(request):
    basket = Basket.objects.filter(user=request.user)
    a1 = Order()
    a1.user = request.user
    a1.address = '665838 Angarsk 22-2-82'
    a1.phone = 89148995893
    a1.save()
    for i in basket:
        a2 = OrderItems()
        a2.order = a1
        a2.product = i.product
        a2.quantity = i.quantity
        a2.save()

    # print(a1.orderitem)
    basket.delete()
    order_form = OrderForm()

    return HttpResponseRedirect(reverse('main'))


def order_list(request):
    order = Order.objects.filter(user=request.user)

    title = 'просмотр заказов'

    content = {'title': title, 'order': order}

    return render(request, 'basketapp/order_list.html', content)


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # if request.method == 'POST':
    order.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    basket_items = OrderItems.objects.filter(order=pk)
    total_quantity = 0
    total_cost = 0
    for item in basket_items:
        total_quantity = total_quantity + int(item.quantity)
        total_cost = total_cost + int(item.quantity) * int(item.product.price)
    content = {'order': order, 'basket_items': basket_items, 'total_quantity': total_quantity, 'total_cost': total_cost}

    return render(request, 'basketapp/order_view.html', content)


def order_pay(request, pk):
    item = get_object_or_404(Order, pk=pk)
    item.status = 'PD'
    item.save()
    order = Order.objects.filter(user=request.user)

    title = 'просмотр заказов'

    content = {'title': title, 'order': order}

    return render(request, 'basketapp/order_list.html', content)
