from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse_lazy

from mainapp.models import Products, ProductCategory


class TestMainappSmoke(TestCase):
    # prepare database object:
    # manage.py dumpdata -e=contenttypes -e=auth -e=sessions -e=social_django
    #                    -e=orderapp.orderitem -o data-dump/test.json
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'data-dump/test.json')
        self.client = Client()

    def test_mainapp_urls_status_code(self):
        SUCCESSFUL_STATUS_CODE = 200
        CHECKING_URLS = (
            '/', '/products/', '/contacts/',
            *[reverse_lazy('products:detail', kwargs=args) for args in Products.objects.values('pk')],
            *[reverse_lazy('products:category', kwargs=args) for args in ProductCategory.objects.values('pk')],
        )
        self.assertTrue(CHECKING_URLS, "Empty CHECKING_URLS")

        for url in CHECKING_URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, SUCCESSFUL_STATUS_CODE, f"Error URL {url}")

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'adminapp', 'orderapp', 'cartapp')


class TestProductsModel(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='TestCase Category')
        self.products = {
            'тестовый товар 1': Products.objects.create(name='тестовый товар 1',
                                                        category=self.category,
                                                        price=199.99, quantity=50),
            'тестовый товар 2': Products.objects.create(name='тестовый товар 2',
                                                        category=self.category,
                                                        price=2000, quantity=1000),
            'тестовый товар 3': Products.objects.create(name='тестовый товар 3',
                                                        category=self.category,
                                                        price=10, quantity=3),
        }

    def test_created_products(self):
        for name, product in self.products.items():
            tmp_products = Products.objects.get(name=name)
            self.assertEqual(tmp_products, product)

    def test_str_method_products(self):
        for name, product in self.products.items():
            self.assertEqual(f"{name} ({product.category.name}, {product.price})", str(product),
                             f"check __str__ function for product {name}")

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'adminapp', 'orderapp', 'cartapp')
