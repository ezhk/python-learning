from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from authapp.forms import LoginForm, CreateForm, EditForm
from authapp.models import ShopUser

from authapp.utils import send_verify_mail


def login(request):
    title = 'Все товары | Войдите'
    next_page = request.GET.get('next', None)

    if request.user and request.user.is_active:
        return HttpResponseRedirect(reverse('index'))

    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        user = auth.authenticate(username=request.POST.get('username', None),
                                 password=request.POST.get('password', None))
        if user and user.is_active:
            auth.login(request, user)
        if request.POST.get('next_page', None) is not None:
            return HttpResponseRedirect(request.POST.get('next_page'))
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'authapp/login.html', {'title': title,
                                                  'login_form': login_form,
                                                  'next_page': next_page})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def create(request):
    title = 'Все товары | Регистрация'

    if request.method == 'POST':
        create_form = CreateForm(request.POST, request.FILES)

        if create_form.is_valid():
            user = create_form.save()
            try:
                if not send_verify_mail(user):
                    raise RuntimeError("Cannot send mail with verify code")
            except Exception as e:
                return render(request, 'authapp/verify.html',
                              {
                                  'header': "Ошибка отправки email",
                                  'error': f"Письмо не было отправлено: {e}"
                              })
            return render(request, 'authapp/verify.html',
                          {
                              'header': "Подтверждение email",
                              'error': "Подтвердите свой электронный адрес по ссылке," + \
                                       f"отправленной на адрес {user.email}",
                          })
            # return HttpResponseRedirect(reverse('auth:login'))
    else:
        create_form = CreateForm()

    return render(request, 'authapp/create.html', {'title': title,
                                                   'create_form': create_form})


def edit(request):
    title = 'Все товары | Профиль'

    if request.method == 'POST':
        edit_form = EditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = EditForm(instance=request.user)

    return render(request, 'authapp/edit.html', {'title': title,
                                                 'edit_form': edit_form})


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        key_object = user.activationkey_set.filter(activation_key=activation_key).first()
        if key_object and key_object.is_active():
            user.is_active = True
            user.save()
            key_object.delete()

            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verify.html')

        return render(request, 'authapp/verify.html',
                      {
                          'header': "Ошибка проверки email",
                          'error': "Не удалось проверить корректность ключа верификации."
                      })
    except Exception as e:
        return render(request, 'authapp/verify.html',
                      {
                          'header': "Проверка email завершена с ошибкой",
                          'error': f"Возникло исключение {e}"
                      })
