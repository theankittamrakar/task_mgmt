from django.contrib.auth import authenticate
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Departments, Projects, Tasks, Teams, Users, Attachments, Status
from .serializers import DepartmentsSerializer, ProjectsSerializer, TasksSerializer, TeamsSerializer, UsersSerializer, \
    UserRegistrationSerializer, UserLoginSerializer, AttachmentsSerializer, StatusSerializer


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response(
                {'data': {'token': str(access), 'refresh': str(refresh)}, "status": True, "detail": "Success"})
        else:
            return Response({'error': 'Invalid credentials', "status": False}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            request.validation_errors = e.detail
            return Response({'status': False, 'detail': 'Validation Error', 'errors': e.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        refresh = RefreshToken.for_user(serializer.instance)
        access = refresh.access_token
        data = {'data': {'token': str(access), 'refresh': str(refresh)}, 'status': True, 'detail': 'Success'}
        headers = self.get_success_headers(serializer.data)
        # 1 / 0
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class TasksListCreateView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            request.validation_errors = e.detail
            return Response({'status': False, 'detail': 'Validation Error', 'errors': e.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        data = {'data': {'status': True, 'detail': 'Success'}}
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer




class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachments.objects.all()
    serializer_class = AttachmentsSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
