from django.contrib.auth.forms import AuthenticationForm,   \
                                      UserCreationForm,     \
                                      UserChangeForm
from authapp.models import ShopUser
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
                  'age', 'gender', 'avatar')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды")

        return data


class EditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password',
                  'firstname', 'lastname',
                  'email',
                  'age', 'gender', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = forms.HiddenInput()
