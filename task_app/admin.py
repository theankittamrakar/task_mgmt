from django.contrib import admin

# Register your models here.
from .models import User, Team, Project

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Project)