from __future__ import unicode_literals
from django.db import models
from accounts.models import CustumUser

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=20, default='test')
    code = models.IntegerField()
    students = models.ManyToManyField(CustumUser, null=True)
