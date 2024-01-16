from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .paginator import CoursesPaginator
from .models import Course, User, Lesson, Comment, Like
from .serializers import CourseSerializer, UserSerializer, LessonSerializer, CommentSerializer, LessonDetailsSerializer
from .perms import OwnerPermissions


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


class LessonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment', 'add_like']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='comment')
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, lesson=self.get_object(),
                                         content=request.data.get('content'))

        return Response(CommentSerializer(comment).data)

    @action(methods=['post'], detail=True, url_path='like')
    def add_like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())

        if not created:
            like.active = not like.active
            like.save()

        return Response(LessonDetailsSerializer(self.get_object(), context={'request': request}).data,
                        status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermissions]
