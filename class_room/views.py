# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Class
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser

# Create your views here.
def index(request):

    try:

        if request.GET.get('error') == '1':
            print('error')
            error = {
                'error': True,
                'message': '선생님만 그룹을 생성할 수 있습니다.'
            }

        else:
            print('not error')
            error = {
                'error': False,
                'message': ''
            }

        user = CustumUser.objects.get(username=request.user)
        return render(request, 'class_room/index.html', {'user': user, 'error': error})

    except:
        return HttpResponseRedirect('accounts/login')


def make_group(request):
    user = CustumUser.objects.get(username=request.user)
    form = Class(code=request.POST.get('code'), name=request.POST.get('name'))

    if user.job == 'teacher':
        if request.method == 'POST':
            newClass = form.save()

        else:
            form = Class()

        group = Class.objects.filter().order_by('name')

        return render(request, 'class_room/make_group.html', {'form' : form, 'groupCnt' : len(group)})

    else:
        return HttpResponseRedirect('/?error=1')

def join_group(request):
    if request.method == 'POST':
        user = CustumUser.objects.get(username=request.user)
        group = Class.objects.get(code=request.POST.get('code'))
        group.students.add(user)
        group.save()

        return HttpResponseRedirect('/')

    return render(request, 'class_room/join_group.html', {'groupCnt' : len(Class.objects.filter())})
