from __future__ import unicode_literals
from django.db import models
from accounts.models import CustumUser
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(CustumUser, related_name="author_set")
    text = models.TextField()
    createdAt = models.DateTimeField(default=timezone.now)

class Class(models.Model):
    teacher = models.ForeignKey(CustumUser, related_name='teacher_set', default=1)
    name = models.CharField(max_length=20, default='test')
    code = models.IntegerField()
    students = models.ManyToManyField(CustumUser, null=True, related_name='student_set')
    requestUser = models.ManyToManyField(CustumUser, null=True, related_name='request_list_set')
    post = models.ManyToManyField(Post, null=True, related_name="post_set")
