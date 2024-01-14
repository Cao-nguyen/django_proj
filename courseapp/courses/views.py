from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from .paginator import CoursesPaginator
from .models import Course, User
from .serializers import CourseSerializer, UserSerializer, LessonSerializer


def index(request):
    return HttpResponse("Hello world!")


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = CoursesPaginator

    # permission_classes = [permissions.IsAuthenticated]

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

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #
    #     return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(subject__icontains=q)

        return queries

    @action(methods=['get'], detail=True)
    def lessons(self, request, pk):
        lessons = self.get_object().lessons.all()

        return Response(LessonSerializer(lessons, many=True, context={'request': request}).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == "list":
    #         return [permissions.AllowAny()]
    #
    #     return [permissions.IsAuthenticated(), ]

