from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Class
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser

# Create your views here.
def index(request):
    user = CustumUser.objects.get(username=request.user)
    return render(request, 'class_room/index.html', {'user' : user})

def make_group(request):
    form = Class(code=request.POST.get('code'), name=request.POST.get('name'))

    if request.method == 'POST':
        newClass = form.save()

    else:
        form = Class()

    group = Class.objects.filter().order_by('name')

    return render(request, 'class_room/make_group.html', {'form' : form, 'groupCnt' : len(group)})
