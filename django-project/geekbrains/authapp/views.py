from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import LoginForm, CreateForm, EditForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'Все товары | Войдите'

    if request.user and request.user.is_active:
        return HttpResponseRedirect(reverse('index'))

    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        user = auth.authenticate(username=request.POST.get('username', None),
                                 password=request.POST.get('password', None))
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'authapp/login.html', {'title': title,
                                                  'login_form': login_form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def create(request):
    title = 'Все товары | Регистрация'

    if request.method == 'POST':
        create_form = CreateForm(request.POST, request.FILES)

        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
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
