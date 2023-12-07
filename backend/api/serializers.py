from rest_framework.serializers import ModelSerializer
from .models import Course, Article


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
