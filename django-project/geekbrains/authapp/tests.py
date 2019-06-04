from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse_lazy

from authapp.models import ShopUser


class TestAuthappSmoke(TestCase):
    # prepare database object:
    # manage.py dumpdata -e=contenttypes -e=auth -e=sessions -e=social_django
    #                    -e=orderapp.orderitem -o data-dump/test.json
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'data-dump/test.json')
        self.client = Client()
        self.USERNAME = {
            'username': 'testCaseUser',
            'firstname': 'testUser',
            'password1': '1azxCdfg3!b',
            'password2': '1azxCdfg3!b',
            'age': 99,
            'email': 'testcaseuser@localhost',
            'gender': 1,
        }

    def test_create_user(self):
        response = self.client.get(reverse_lazy('authapp:create'));
        self.assertEqual(response.context.get('title'), 'Все товары | Регистрация',
                         f"Wrong title header in URL {reverse_lazy('authapp:create')}")
        self.assertTrue(response.context.get('user').is_anonymous)

        response = self.client.post(reverse_lazy('authapp:create'), data=self.USERNAME, )
        self.assertTrue("Подтвердите свой электронный адрес по ссылке," +
                        f"отправленной на адрес {self.USERNAME.get('email')}" in response.content.decode("utf-8"))

        user_object = ShopUser.objects.get(username=self.USERNAME.get('username'))
        activation_key = user_object.activationkey_set.values_list(
            'activation_key', flat=True
        ).first()
        self.assertTrue(activation_key, "Wrong activation key")

        response = self.client.get(reverse_lazy('authapp:verify', kwargs={'email': self.USERNAME.get('email'),
                                                                          'activation_key': activation_key, }))
        self.assertTrue('Спасибо за регистрацию' in response.content.decode("utf-8"))

        response = self.client.get('/')
        self.assertTrue(self.USERNAME.get('username')[0].capitalize() + self.USERNAME.get('username')[1:]
                        in response.content.decode("utf-8"))

    def test_login_logout(self):
        user = ShopUser.objects.create(username=self.USERNAME.get('username'))
        user.set_password(self.USERNAME.get('password1'))
        user.save()

        self.assertTrue(self.client.login(username=self.USERNAME.get('username'),
                                          password=self.USERNAME.get('password1')))

        response = self.client.get(reverse_lazy('authapp:login'))
        # print(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('index'))

        # check that user authenticated
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get(reverse_lazy('authapp:logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_redirect_cart(self):
        user = ShopUser.objects.create(username=self.USERNAME.get('username'))
        user.set_password(self.USERNAME.get('password1'))
        user.save()

        response = self.client.get(reverse_lazy('cart:index'))
        self.assertEqual(response.url,
                         str(reverse_lazy('authapp:login')) +
                         '?next=' + str(reverse_lazy('cart:index')))

        self.assertTrue(self.client.login(username=self.USERNAME.get('username'),
                                          password=self.USERNAME.get('password1')))
        response = self.client.get(reverse_lazy('cart:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('title'), 'Все товары | Корзина')

    def test_wrong_create(self):
        local_username = self.USERNAME.copy()
        local_username.update({'username': 'wrongUser',
                              'email': 'wronguser@localhost',
                              'age': 17, })
        response = self.client.post(reverse_lazy('authapp:create'), data=local_username, )
        self.assertTrue('Вы слишком молоды' in response.content.decode("utf-8"))
