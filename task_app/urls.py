from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, AttachmentsViewSet, StatusViewSet, UserRegistrationView, \
    TasksListCreateView, UserLoginView, TaskRetrieveUpdateDestroyView, TeamRetrieveUpdateDestroyView, \
    TeamListCreateView, TeamListUsersView, TeamListProjectsView, ProjectListView, ProjectRetrieveUpdateDestroyView

router = DefaultRouter()

# router.register(r'teams', TeamsViewSet, basename='teams')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'attachments', AttachmentsViewSet, basename='attachments')
router.register(r'status', StatusViewSet, basename='status')


urlpatterns = [
    path('', include(router.urls)),
    # path('', views.ApiRoot.as_view(), name='views.ApiRoot.name'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),

    path('tasks/', TasksListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),

    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('teams/<int:pk>/', TeamRetrieveUpdateDestroyView.as_view(), name='team-retrieve-update-destroy'),
    path('teams/<int:pk>/users/', TeamListUsersView.as_view(), name='team-users'),
    path('teams/<int:pk>/projects/', TeamListProjectsView.as_view(), name='team-projects'),

    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update'),
]

