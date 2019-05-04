from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now
from datetime import timedelta


class ShopUser(AbstractUser):
    GENDER_TYPE_CHOICES = (
        (-1, 'Не указан'),
        (0, 'Женский'),
        (1, 'Мужской')
    )

    email = models.EmailField(verbose_name='email', max_length=256, unique=True)

    firstname = models.CharField(verbose_name='Имя', max_length=64, null=True)
    lastname = models.CharField(verbose_name='Фамилия', max_length=128, blank=True)

    gender = models.SmallIntegerField(verbose_name='Пол', choices=GENDER_TYPE_CHOICES, default=-1)
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True)

    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars', blank=True)
    is_active = models.BooleanField(verbose_name='Активный пользователь', default=True)


class ActivationKey(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)

    activation_key = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        if now() - timedelta(hours=48) <= self.created_at:
            return True
        return False
