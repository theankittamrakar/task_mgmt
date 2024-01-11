from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel


class Team(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the name of the team")

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the name of the project")
    team = models.ForeignKey(Team, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    first_name = models.CharField(blank=False, max_length=100)
    last_name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    teams = models.ManyToManyField(Team, related_name='users', blank=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team, related_name='tasks', blank=True)
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # done = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Attachment(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file = models.FileField(upload_to='attachments/')
    attachment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    attachment_id = models.PositiveIntegerField()
    attachment = GenericForeignKey('attachment_type', 'attachment_id')

    def __str__(self):
        return self.name


class Status(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_current = models.BooleanField(default=True)
    status_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    status_id = models.PositiveIntegerField()
    status = GenericForeignKey('status_type', 'status_id')

    def __str__(self):
        return self.name
