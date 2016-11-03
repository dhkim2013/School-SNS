# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreateForm
from django.contrib.auth import authenticate,login, models
from .models import CustumUser
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout

# Create your views here.
def register(request):
    logout(request)
    form = UserCreateForm(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            newUser = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/')

    else:
        form = UserCreateForm()

    return render(request, 'accounts/register.html', { 'form': form })

def login(request):
    logout(request)
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')

        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})

    return render(request, 'accounts/login.html')

def profile(request):
    user = CustumUser.objects.get(username=request.user)
    return render(request, 'accounts/profile.html', { 'user': user })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
