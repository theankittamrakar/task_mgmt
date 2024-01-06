from django.contrib import admin

# Register your models here.
from .models import Users, Departments, Projects

admin.site.register(Users)