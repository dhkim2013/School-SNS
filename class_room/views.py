# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Class
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser

# Create your views here.
def index(request):

    try:
        user = CustumUser.objects.get(username=request.user)

        if user.hasGroup == True:
            return render(request, 'class_room/mygroup.html')

        else :
            return render(request, 'class_room/index.html', {'user': user})

    except:
        return HttpResponseRedirect('accounts/login')


def make_group(request):
    user = CustumUser.objects.get(username=request.user)
    form = Class(teacher=user, code=request.POST.get('code'), name=request.POST.get('name'))

    if user.job == 'teacher':
        if request.method == 'POST':
            newClass = form.save()

        else:
            form = Class()

        group = Class.objects.filter().order_by('name')
        user.hasGroup = True
        user.save()

        if user.hasGroup is False:
            return render(request, 'class_room/make_group.html', {'form' : form, 'groupCnt' : len(group)})

    return HttpResponseRedirect('/')

def join_group(request):
    if request.method == 'POST':
        user = CustumUser.objects.get(username=request.user)
        group = Class.objects.get(code=request.POST.get('code'))
        group.students.add(user)
        group.save()
        user.hasGroup = True
        user.save()

        return HttpResponseRedirect('/')

    return render(request, 'class_room/join_group.html', {'groupCnt' : len(Class.objects.filter())})

def search_group(request):

    if request.method == 'GET':
        code = request.GET.get('code')
        hasData = False

        if (code != None) and (code != ''):
            result = Class.objects.filter(code=int(code)).order_by('pk')

            if len(result) == 1:
                hasData = True

            return render(request, 'class_room/search_group.html', {'result': result, 'hasData': hasData})

        return render(request, 'class_room/search_group.html', {'hasData': hasData})

    elif request.method == 'POST':
        print(request.POST.get('pk'))
        group = Class.objects.get(pk=int(request.POST.get('pk')))
        user = CustumUser.objects.get(username=request.user)
        group.requestUser.add(user)
        group.save()

        return render(request, 'class_room/request_finish.html')
