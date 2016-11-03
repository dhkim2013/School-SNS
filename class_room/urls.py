from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^make_group/', views.make_group, name='make_group'),
    url(r'^join_group/', views.join_group, name='join_group'),
    url(r'^search_group/', views.search_group, name='search_group'),
]
