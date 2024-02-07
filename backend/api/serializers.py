from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Article, CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None


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
