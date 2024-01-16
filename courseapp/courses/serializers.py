from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Category, User, Tag, Lesson, Comment


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BaseSerializer(ModelSerializer):
    image = SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    def get_image(self, course):
        if course.image:
            path = "/static/%s" % course.image.name
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(path)
            return path


class CourseSerializer(BaseSerializer):
    image = SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "subject", "created_date", "description", "image", "active", "category", 'tags']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'is_active', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user


class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'content', 'image', 'course']


class LessonDetailsSerializer(LessonSerializer):
    liked = SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return lesson.like_set.filter(active=True).exists()

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['liked']


class CommentSerializer(ModelSerializer):
    user = UserSerializer()
    lesson = LessonSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'lesson', 'user']
