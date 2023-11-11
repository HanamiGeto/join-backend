from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from join.models import Task
from join.serializers import TaskSerializer, UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class TaskList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.filter(author=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class TaskDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        tasks = Task.objects.filter(pk=pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk, format=None):
        task = Task.objects.filter(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)