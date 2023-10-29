from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="uploads/%y/%m")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="courses/%Y/%m")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ("subject", "category")


class Lesson(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="lessons/%Y/%m")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("subject", "category")


class Tag(models.Model):
    name = models.CharField(max_length=255)
