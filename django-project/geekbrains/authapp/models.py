from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    GENDER_TYPE_CHOICES = (
        (-1, 'Не указан'),
        (0, 'Женский'),
        (1, 'Мужской')
    )

    firstname = models.CharField(verbose_name='Имя', max_length=64, null=True)
    lastname = models.CharField(verbose_name='Фамилия', max_length=128, blank=True)

    gender = models.SmallIntegerField(verbose_name='Пол', choices=GENDER_TYPE_CHOICES, default=-1)
    age = models.PositiveIntegerField(verbose_name='Возраст')

    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars', blank=True)
