# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PostForm, CommentForm
from accounts.forms import ProfileForm
from django.contrib.auth import authenticate,login, models
from accounts.models import CustumUser
from .models import Post, Comment, Class
from django.db.models import Q

# Create your views here.
def index(request):

    # try:
    user = CustumUser.objects.get(username=request.user)

    if user.hasGroup == True:

        if user.job == 'teacher':
            group = Class.objects.get(teacher=user)

        else:
            group = Class.objects.all().filter(students=user)[0]

        if request.method == 'POST':

            if request.POST['keyword']:
                posts = group.post.filter(Q(title__contains=request.POST['keyword'])).order_by('-pk')
                return render(request, 'class_room/mygroup.html', {'group': group, 'posts': posts, 'user': user})

            else:
                form = CommentForm(request.POST)
                comment = form.save(commit=False)
                comment.writer = CustumUser.objects.get(username=request.user)
                comment.save()
                group.post.get(pk=request.POST.get('pk')).comment.add(comment)
                group.save()

                return HttpResponseRedirect('/')

        posts = group.post.filter().order_by('-pk')

        return render(request, 'class_room/mygroup.html', {'group': group, 'posts': posts, 'user': user})

    else :
        return render(request, 'class_room/index.html', {'user': user})

    # except:
    #     return HttpResponseRedirect('/accounts/login')

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
            myClass = Class.objects.get(teacher=user)

            for i in myClass.students.all():
                i.hasGroup = False
                i.save()

            myClass.delete()

        else:
            Class.objects.all().filter(students=user)[0].students.get(username=user.username).delete()

        user.hasGroup = False
        user.save()

    return HttpResponseRedirect('/')

def setting(request):
    user = CustumUser.objects.get(username=request.user)

    if user.job == 'teacher':
        group = Class.objects.get(teacher=user)

    else:
        group = Class.objects.all().get(students=user)

    reqUserList = group.requestUser.all()

    if request.GET.get('accept') == '1':
        reqUser = CustumUser.objects.get(pk=request.GET.get('pk'))

        if reqUser.hasGroup == False:
            reqUser.hasGroup = True
            group.requestUser.get(pk=request.GET.get('pk')).delete()
            group.students.add(reqUser)
            reqUser.save()
            group.save()

        return HttpResponseRedirect('/setting')

    if request.GET.get('accept') == '0':
        reqUser = CustumUser.objects.get(pk=request.GET.get('pk'))

        if reqUser.hasGroup == False:
            group.requestUser.get(pk=request.GET.get('pk')).delete()
            reqUser.save()
            group.save()

        return HttpResponseRedirect('/setting')

    if request.method == 'POST':
        handle_uploaded_file(request.FILES.get('profileImage'), user.username)
        user.profileImage = 'profiles/' + user.username + '.jpg'
        user.introduce = request.POST.get('introduce')
        user.save()

        return HttpResponseRedirect('/setting')

    return render(request, 'class_room/setting_group.html', {'group': group, 'reqUserList': reqUserList, 'user': user})

def handle_uploaded_file(f, name):

    if f is not None:

        with open('media/profiles/' + name + '.jpg', 'wb+') as destination:

            for chunk in f.chunks():
                destination.write(chunk)

def profile(request):
    user = CustumUser.objects.get(username=request.user)

    if user.job == 'teacher':
        group = Class.objects.get(teacher=user)

    else:
        group = Class.objects.all().get(students=user)

    if request.method == 'POST':

        print(request.FILES[profileImage])
        if request.FILES.get('profileImage') is not None:
            handle_uploaded_file(request.FILES.get('profileImage'), user.username)
            user.profileImage = 'profiles/' + user.username + '.jpg'
            print('test')

        user.introduce = request.POST.get('introduce')
        user.save()

    return render(request, 'class_room/profile.html', {'group': group, 'user': user})
