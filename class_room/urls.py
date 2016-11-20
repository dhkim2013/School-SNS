from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^make_group/', views.make_group, name='make_group'),
    url(r'^search_group/', views.search_group, name='search_group'),
    url(r'^new_post/', views.new_post, name='new_post'),
    url(r'^exit_group/', views.exit_group, name='exit_group'),
    url(r'^setting/', views.setting, name='setting'),
    url(r'^notice/', views.notice, name='notice'),
    url(r'^board/', views.board, name='board')
]
