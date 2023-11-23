from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to="uploads/%y/%m")


class BaseModels(models.Model):
    subject = models.CharField(max_length=100, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class Course(BaseModels):
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="images/courses/%Y/%m")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ("subject", "category")
        ordering = ['id']


class Lesson(BaseModels):
    content = RichTextField(null=True)
    image = models.ImageField(upload_to="images/lesson/%Y/%m")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name="lessons", blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ("subject", "course")


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
