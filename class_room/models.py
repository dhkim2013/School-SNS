from __future__ import unicode_literals
from django.db import models
from accounts.models import CustumUser

# Create your models here.
class Class(models.Model):
    teacher = models.ForeignKey(CustumUser, related_name='teacher_set', default=1)
    name = models.CharField(max_length=20, default='test')
    code = models.IntegerField()
    students = models.ManyToManyField(CustumUser, null=True, related_name='student_set')
