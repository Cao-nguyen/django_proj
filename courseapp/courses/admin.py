from django.contrib import admin
from .models import Category, Course, Lesson, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    search_fields = ['subject']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Tag)

