from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from ordersapp.models import Order
from django.views.generic import DeleteView
from ordersapp.models import OrderItem
from ordersapp.forms import OrderCreateForm
from basketapp.models import Basket

def OrderCreate(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            basket.clear()
            return render(request, 'ordersapp/created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'ordersapp/create.html', {'basket': basket,
                                                        'form': form})

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')
