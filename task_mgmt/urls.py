"""
URL configuration for task_mgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_app.views import (DepartmentsViewSet, ProjectsViewSet, TasksViewSet, TeamsViewSet, UsersViewSet,
                            UserRegistrationView, UserLoginView)

router = DefaultRouter()
router.register(r'departments', DepartmentsViewSet, basename='departments')
router.register(r'projects', ProjectsViewSet, basename='projects')
router.register(r'tasks', TasksViewSet, basename='tasks')
router.register(r'teams', TeamsViewSet, basename='teams')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-view')
]

