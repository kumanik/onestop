from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import *


def login_view(request):
    if request.user.is_authenticated():
        logout(request)
    nxt = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if nxt:
            return redirect(nxt)
        return redirect('/')

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    nxt = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if nxt:
            return redirect(nxt)
        return redirect('/')

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, '/')