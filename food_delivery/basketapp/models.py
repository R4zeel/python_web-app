from django.db import models
from django.conf import settings
from mainapp.models import Products, ProductCompany


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=20, decimal_places=2, default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    product_cost = property(get_product_cost)

    def get_total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        return totalquantity

    total_quantity = property(get_total_quantity)

    def _get_total_cost(self):
        items = Basket.objects.filter(user=self.user)
        totalcost = sum(list(map(lambda x: x.product_cost, items)))
        return totalcost

    total_cost = property(_get_total_cost)

    def get_items(user):
        items = Basket.objects.filter(user=user)
        return items

    items = property(get_items)