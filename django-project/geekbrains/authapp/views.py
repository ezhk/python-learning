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

    content = {'title': title}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def create(request):
    title = 'Все товары | Регистрация'

    if request.method == 'POST':
        register_form = CreateForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = CreateForm()

    content = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/create.html', content)


def edit(request):
    title = 'Все товары | Профиль'

    if request.method == 'POST':
        edit_form = EditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = EditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)
