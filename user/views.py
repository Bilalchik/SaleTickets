from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import UserRegisterForm


def user_register_view(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('index')

    for field, errors in form.errors.items():

        for error in errors:
            messages.error(request, f'{error}')

    return redirect('index')


def user_login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        user = authenticate(
            request=request,
            username=phone_number,
            password=password
        )

        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')

            return redirect('index')

        messages.error(request, 'Неверный логин или пароль.')

    return redirect('index')


def user_logout_view(request):

    logout(request)

    return redirect('index')


