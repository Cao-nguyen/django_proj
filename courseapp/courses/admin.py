from django.contrib import admin
from .models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description', 'active', 'category']
    search_fields = ['subject']


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm


class CourseAppAdminSite(admin.AdminSite):
    site_header = "KHÓA HỌC TRỰC TUYẾN"


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson)
# admin.site.register(Tag)

admin_site = CourseAppAdminSite(name="courses")
admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)
