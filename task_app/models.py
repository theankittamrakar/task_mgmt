from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel


class Departments(models.Model):
    name = models.CharField(max_length=100)


class Projects(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Tasks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


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


class Attachments(PolymorphicModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file = models.FileField(upload_to='attachments/')
    attachment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attachment_id = models.PositiveIntegerField()
    attachment = GenericForeignKey('attachment_type', 'attachment_id')


class Status(PolymorphicModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_current = models.BooleanField(default=True)
    status_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    status_id = models.PositiveIntegerField()
    status = GenericForeignKey('status_type', 'status_id')
