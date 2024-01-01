from django.db import models
from django.contrib.auth.models import AbstractUser


class Departments(models.Model):
    name = models.CharField(max_length=100)


class Projects(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Tasks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class Teams(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Projects, related_name='teams', blank=True)
    tasks = models.ManyToManyField(Tasks, related_name='teams', blank=True)


class Users(AbstractUser):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Tasks, related_name='users', blank=True)
    teams = models.ManyToManyField(Teams, related_name='users', blank=True)
