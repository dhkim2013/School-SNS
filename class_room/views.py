# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser
from .models import Post, Comment, Class

# Create your views here.
def index(request):

    try:
        user = CustumUser.objects.get(username=request.user)

        if user.hasGroup == True:

            if user.job == 'teacher':
                group = Class.objects.get(teacher=user)

            else:
                group = Class.objects.all().filter(students=user)[0]

            if request.method == 'POST':
                print(request.POST)
                form = CommentForm(request.POST)
                comment = form.save(commit=False)
                comment.writer = CustumUser.objects.get(username=request.user)
                comment.save()
                group.post.get(pk=request.POST.get('pk')).comment.add(comment)
                group.save()

                return HttpResponseRedirect('/')

            posts = group.post.filter().order_by('-pk')

            return render(request, 'class_room/mygroup.html', {'group': group, 'posts': posts})

        else :
            return render(request, 'class_room/index.html', {'user': user})

    except:
        return HttpResponseRedirect('/accounts/login')

def make_group(request):
    user = CustumUser.objects.get(username=request.user)
    print(user)

    if user.job == 'teacher':
        if request.method == 'POST':
            form = Class(teacher=user, code=request.POST.get('code'), name=request.POST.get('name'))
            newClass = form.save()

        else:
            form = Class()

        group = Class.objects.filter().order_by('name')

        if user.hasGroup is False:
            user.hasGroup = True
            user.save()
            return render(request, 'class_room/make_group.html', {'form' : form, 'groupCnt' : len(group)})

    return HttpResponseRedirect('/')

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

def new_post(request):

    try:
        user = CustumUser.objects.get(username=request.user)

        if user.hasGroup == True:

            if user.job == 'teacher':
                group = Class.objects.get(teacher=user)

            else:
                group = Class.objects.all().filter(students=user)[0]

            if request.method == 'POST':
                form = PostForm(request.POST)
                post = form.save(commit=False)
                post.author = CustumUser.objects.get(username=request.user)
                post.save()
                group.post.add(post)
                group.save()

                return HttpResponseRedirect('/')

            return render(request, 'class_room/new_post.html', {'group': group, 'user': user})

        else :
            return render(request, 'class_room/index.html', {'user': user})

    except:
        return HttpResponseRedirect('/accounts/login')

def exit_group(request):

    print(request.user)

    user = CustumUser.objects.get(username=request.user)

    if user.hasGroup == True:

        if user.job == 'teacher':
            print('teacher')
            Class.objects.get(teacher=user).delete()

        else:
            print('student')
            Class.objects.all().filter(students=user)[0].students.get(username=user.username).delete()

        user.hasGroup = False
        user.save()

    return HttpResponseRedirect('/')

def setting(request):
    user = CustumUser.objects.get(username=request.user)

    if user.job == 'teacher':
        group = Class.objects.get(teacher=user)

    else:
        group = Class.objects.all().filter(students=user)[0]

    reqUser = group.requestUser.all()

    if request.GET.get('accept') == '1':
        user = CustumUser.objects.get(username=group.requestUser.get(pk=request.GET.get('pk')).username)

        if user.hasGroup == False:
            user.hasGroup = True
            group.requestUser.get(pk=request.GET.get('pk')).delete()
            group.students.add(user)
            user.save()
            group.save()

    if request.GET.get('accept') == '0':
        user = CustumUser.objects.get(username=group.requestUser.get(pk=request.GET.get('pk')).username)

        if user.hasGroup == False:
            group.requestUser.get(pk=request.GET.get('pk')).delete()
            user.save()
            group.save()

    me = CustumUser.objects.get(username=request.user)

    return render(request, 'class_room/setting_group.html', {'group': group, 'user': reqUser, 'me': me})
