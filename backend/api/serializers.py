from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Article


class CourseSerializer(ModelSerializer):

    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        request = self.context.get('request')
        if obj.pic:
            return request.build_absolute_uri(obj.pic.url)
        return None

    class Meta:
        model = Course
        fields = '__all__'


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
