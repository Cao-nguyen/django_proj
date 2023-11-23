from .models import Course, Category
from django.db.models import Count


def count_course():
    return Course.objects.count()


def count_lesson_in_course():
    return Course.objects.annotate(lesson_count=Count('lessons')).values('id', 'subject', 'lesson_count')
