from django.db import models


class ProductCompany(models.Model):
    name = models.CharField(verbose_name='наименование компании', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание компании', blank=True)
    image = models.ImageField(upload_to='company_images', blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='наименование категории', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание категории', blank=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    company = models.ForeignKey(ProductCompany, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='наименование продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)

    def __str__(self):
        return "{0} ({1}) ({2})".format(self.name, self.category.name, self.company.name)
