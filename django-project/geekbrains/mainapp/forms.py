from django import forms
from mainapp.models import FeedBack


class FeedBackForm(forms.Form):
    class Meta:
        model = FeedBack
        fields = '__all__'

    username = forms.CharField(label='Имя пользователя', max_length=64)
    email = forms.EmailField(label='Электронная почта', max_length=128)
    subject = forms.CharField(label='Тема', max_length=100)
    body = forms.CharField(label='Сообщение', max_length=1024, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(FeedBackForm, self).__init__(*args, **kwargs)

        self.fields.get('username').required = False
        self.fields.get('subject').required = False
