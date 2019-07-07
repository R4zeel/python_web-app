from django.core.management.base import BaseCommand
import mainapp.models as mainapp

import json, os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # категории
        categories = load_from_json('categories')
        mainapp.ProductCategory.objects.all().delete()
        for category in categories:
            new_category = mainapp.ProductCategory(**category)
            new_category.save()


        # рестораны
        companies = load_from_json('companies')
        mainapp.ProductCompany.objects.all().delete()
        for company in companies:
            new_company = mainapp.ProductCompany(**company)
            new_company.save()

        # продукты
        products = load_from_json('products')
        mainapp.Products.objects.all().delete()
        for product in products:
            new_product = mainapp.Products(**product)
            new_product.save()
