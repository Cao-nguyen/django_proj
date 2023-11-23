from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Count
from .models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from . import dao


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'


class CourseInlineAdmin(admin.StackedInline):
    model = Course
    fk_name = "category"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id']
    inlines = [CourseInlineAdmin, ]


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description', 'active', 'category']
    search_fields = ['subject']
    inlines = [LessonInlineAdmin, ]


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    list_display = ['id', 'subject', 'content', 'image', 'course']


class CourseAppAdminSite(admin.AdminSite):
    site_header = "KHÓA HỌC TRỰC TUYẾN"

    def get_urls(self):
        return [
                   path('admin_stats/', self.admin_stats)
               ] + super().get_urls()

    def admin_stats(self, request):
        count = dao.count_course()
        stats = dao.count_lesson_in_course()
        return TemplateResponse(request, "admin/course_stats.html", {
            'count_course': count,
            'stats': stats
        })


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson)
# admin.site.register(Tag)

admin_site = CourseAppAdminSite(name="courses")
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)
