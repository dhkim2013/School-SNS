from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class CustumUser(User):
    name = models.CharField(max_length=20, default="none")
    job = models.CharField(max_length=10)
    hasGroup = models.BooleanField(default=False)
    profileImage = models.ImageField(upload_to="profiles/", default="profiles/default.jpg")
    introduce = models.CharField(max_length=100, default='')
