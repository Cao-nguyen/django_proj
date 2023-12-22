from rest_framework.serializers import ModelSerializer
from .models import Course, Category, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "subject", "created_date", "description", "image", "active", "category"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'is_active']

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user
