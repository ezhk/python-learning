from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    GENDER_TYPE_CHOICES = (
        (-1, 'undefined'),
        (0, 'female'),
        (1, 'male')
    )

    firstname = models.CharField(verbose_name='name', max_length=64, null=True)
    lastname = models.CharField(verbose_name='surname', max_length=128, blank=True)

    gender = models.SmallIntegerField(choices=GENDER_TYPE_CHOICES, default=-1)
    age = models.PositiveIntegerField(verbose_name='age')

    avatar = models.ImageField(upload_to='avatars', blank=True)
