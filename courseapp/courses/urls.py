from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('courses', views.CourseViewSet)
router.register('user', views.UserViewSet)
router.register('lesson', views.LessonViewSet)
router.register('comment', views.CommentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls)
]
