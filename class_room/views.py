from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Class
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser

# Create your views here.
def index(request):
    user = CustumUser.objects.get(username=request.user)
    return render(request, 'class_room.index.html', {'user' : user})
