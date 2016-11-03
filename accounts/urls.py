from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^logout/', views.logout_view, name='logout_view'),
]
