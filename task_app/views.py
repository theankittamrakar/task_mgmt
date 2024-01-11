from django.contrib.auth import authenticate
from rest_framework import mixins
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Project, Task, Team, User, Attachment, Status
from .permissions import IsManager, IsMember
from .serializers import ProjectSerializer, TaskSerializer, TeamSerializer, UserSerializer, \
    UserRegistrationSerializer, UserLoginSerializer, AttachmentSerializer, StatusSerializer, UserInTeamSerializer, \
    ProjectsOfTeamSerializer
from .utils import StandardResultsSetPagination


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            request.validation_errors = e.detail
            return Response({'status': False, 'detail': 'Validation Error', 'errors': e.detail},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # print(f"Email: {email}")
        # print(f"Password: {password}")

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response(
                {'data': {'token': str(access), 'refresh': str(refresh)}, "status": True, "detail": "Success"},
                status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials', "status": False}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    name = "registration"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            request.validation_errors = e.detail
            return Response({'status': False, 'detail': 'Validation Error', 'errors': e.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        # refresh = RefreshToken.for_user(serializer.instance)
        # access = refresh.access_token
        # data = {'data': {'token': str(access), 'refresh': str(refresh)}, 'status': True, 'detail': 'Success'}
        data = {'data': {'status': True, 'detail': 'Success'}}

        headers = self.get_success_headers(serializer.data)
        # 1 / 0
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class TasksListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination

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


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


# custom roles and permissions

class TeamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamListUsersView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Team.objects.all()
    serializer_class = UserInTeamSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        team = self.get_object()
        users = team.users.all()
        serializer = UserInTeamSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamListProjectsView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Team.objects.all()
    serializer_class = ProjectsOfTeamSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        team = self.get_object()
        projects = team.projects.all()
        serializer = ProjectsOfTeamSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectListView(TeamListCreateView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

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


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, mixins.ListModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = StandardResultsSetPagination  # Make sure to import StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsMember()]
        elif self.request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsManager()]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
