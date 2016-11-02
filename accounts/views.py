from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreateForm
from django.contrib.auth import authenticate,login, models
from .models import CustumUser

# Create your views here.
def register(request):
    form = UserCreateForm(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            newUser = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/login/')

    else:
        form = UserCreateForm()

    return render(request, 'accounts/register.html', { 'form': form })

def profile(request):
    user = CustumUser.objects.get(username=request.user)
    return render(request, 'accounts/profile.html', { 'user' : user })
