from datetime import datetime, timedelta
import logging
import os
import requests
from urllib.parse import urlparse

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from django.utils.timezone import now

logger = logging.getLogger(__name__)


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

    is_active = models.BooleanField(verbose_name='Активный пользователь', default=True)

    def validate_age(self, user_about_url=None):
        if self.age:
            return False if (self.age < 18) else True
        if user_about_url is None:
            return None

        try:
            r = requests.get(user_about_url)
            if r.status_code != 200:
                raise ValueError(f"{user_about_url} returned {r.status_code} status code")
            response = r.json().get('response', [])
            if not response:
                return None

            response = response.pop()
            if not response.get('bdate', None):
                return None
            age = datetime.now() - datetime.strptime(response.get('bdate'), '%d.%m.%Y')
            age = age.days // 365.25

            if age < 18:
                return False

            self.age = age
            self.save()
        except Exception as e:
            logger.error(f"validate_age exception {e}")
            return None

        return True


class ShopUserExtended(models.Model):
    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)

    userpic = models.ImageField(verbose_name='Аватар', upload_to='userpic', blank=True)
    tags = models.CharField(verbose_name='Теги', max_length=128, blank=True)
    about = models.CharField(verbose_name='О себе', max_length=128, blank=True)

    # on_delete CASCADE helps us to make it easy
    @receiver(pre_delete, sender=ShopUser)
    def pre_delete_receiver(sender, instance, **kwargs):
        user = ShopUserExtended.objects.get(user=instance)
        if user.userpic and user.userpic.path:
            os.unlink(user.userpic.path)
        return ShopUserExtended.objects.filter(user=instance).delete()

    @receiver(post_save, sender=ShopUser)
    def post_save_receiver(sender, instance, created, **kwargs):
        if created:
            return ShopUserExtended.objects.create(user=instance)
        return instance.shopuserextended.save()

    def udpate_userpic(self, userpic_url=None, refresh=False):
        if self.userpic and not refresh:
            return True

        try:
            r = requests.get(userpic_url)
            if r.status_code != 200:
                raise ValueError(f"{userpic_url} returned {r.status_code} status code")

            userpic_name = urlparse(userpic_url)
            userpic_name = os.path.basename(userpic_name.path)

            userpic_temporary = NamedTemporaryFile(delete=True)
            userpic_temporary.write(r.content)
            userpic_temporary.flush()

            self.userpic.save(f"{self.user.username}_{userpic_name}",
                              File(userpic_temporary))
        except Exception as e:
            logger.error(f"udpate_userpic exception {e}")
            return False

        return True


class ActivationKey(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)

    activation_key = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        if now() - timedelta(hours=48) <= self.created_at:
            return True
        return False
