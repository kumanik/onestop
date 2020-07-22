from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, UserLoginForm
from accounts.models import api_key


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        if request.next is not None:
            request.next = '/accounts/check_staff'
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("check_staff")
        else:
            messages.error("Wrong username or password")
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        key = api_key(user=new_user)
        key.save()
        return redirect('check_staff')
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, '/')

def check_staff(request):
    if request.user.is_staff:
        return redirect('/home')
    else:
        return render(request, 'registration/not_authorized.html')