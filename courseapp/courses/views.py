from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import views
from .models import Course, User
from .serializers import CourseSerializer, UserSerializer


def index(request):
    return HttpResponse("Hello world!")


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer

    @action(methods=['put'], detail=True)
    def hide_course(self, request, pk):
        try:
            c = Course.objects.get(pk=pk)
            c.active = False
            c.save()
        except Course.DoesNotExits:
            return Response("404 not found")

        serializer = CourseSerializer(c)
        return Response(data=serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
