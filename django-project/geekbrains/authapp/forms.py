import hashlib
import random
import string

from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, \
    UserChangeForm
from authapp.models import ShopUser, \
    ShopUserExtended, \
    ActivationKey
from django import forms


class LoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')


class CreateForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username',
                  'firstname', 'lastname',
                  'password1', 'password2',
                  'email',
                  'age', 'gender')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды")

        return data

    def save(self):
        user = super(CreateForm, self).save()

        user.is_active = False
        user.save()

        salt = ''.join([random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase +
                                      string.digits)
                        for _ in range(16)])
        activation_key = hashlib.sha256(
            (user.email + salt).encode('utf8')
        ).hexdigest()
        ActivationKey(user=user, activation_key=activation_key).save()

        return user


class EditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password',
                  'firstname', 'lastname',
                  'email',
                  'age', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class ShopUserExtendedForm(forms.ModelForm):
    class Meta:
        model = ShopUserExtended
        fields = ('userpic', 'tags', 'about')
