from django.urls import path
from .views import TasksListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    # path('tasks/', TasksListCreateView.as_view(), name='tasks-list-create'),
    # path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='tasks_retrieve-update-destroy')
]
