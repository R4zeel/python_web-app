from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserEditForm
from authapp.forms import ShopUserRegisterForm
from django.contrib import auth
from django.urls import reverse
from authapp.models import ShopUser


def login(request):
    title = 'Вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    if 'next' in request.POST.keys():
        next = request.POST['next']
    else:
        next = str(request.META.get('HTTP_REFERER'))
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:

            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {'title': title, 'login_form': login_form, 'next': next}

    # return redirect(return_path)

    return render(request, 'authapp/login.html', content)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            # if send_verify_mail(user):
            #     print('сообщение подтвердтверждения отправлено')
            return HttpResponseRedirect(reverse('auth:login'))
            # else:
            #     print('ошибка отправки сообщения')
            #     return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, instance=request.user)


        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)


    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)