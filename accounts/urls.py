from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^register/', views.register, name='register'),
    url('^profile/', views.profile, name='profile'),
]
