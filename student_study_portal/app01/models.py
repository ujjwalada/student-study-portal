from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import User
# # Create your models here.


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
   #  ye wala def se admin pannel pe title show hoga

    def __str__(self):
        return self.title


# model for homework


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField()

    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
