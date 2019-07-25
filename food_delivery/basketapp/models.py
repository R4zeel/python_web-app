from django.db import models
from django.conf import settings
from mainapp.models import Products, ProductCategory, Restaurant


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    restauran = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
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


class Order(models.Model):
    FORMING = 'FM'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    DELIVERED = 'DLV'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'собирается'),
        (READY, 'передан на доставку'),
        (DELIVERED, 'доставлен'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField(verbose_name='Адрес доставки', max_length=300)
    phone = models.PositiveIntegerField(verbose_name='Телефон', default=8)
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_restaurant(self):
        item = OrderItems.objects.filter(order=self.id).first()
        return item.product.restaurant

    def get_products(self):
        items = OrderItems.objects.filter(order=self.id)
        product_list = ''
        for item in items:
            product_list += item.product.name
        return product_list

    def get_total_quantity(self):
        print(5554444)
        items = OrderItems.objects.filter(order=order.pk)

        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = OrderItems.objects.filter(order=self.pk)
        print(items)
        return len(items)

    def get_total_cost(self):
        items = OrderItems.objects.filter(order=self.pk)
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))


class OrderItems(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(self, pk):
        return OrderItem.objects.filter(pk=pk).first()
