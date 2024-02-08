from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Article, CustomUser, Topic, Lecture, Answers,Question,Module


class AnswersSerializer(ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    answer = serializers.SerializerMethodField()

    def get_answer(self, obj):
        answers = Answers.objects.filter(question=obj)
        answer_serializer = AnswersSerializer(answers, many=True)
        return answer_serializer.data
    class Meta:
        model = Question
        fields = ['question', 'answer']


class ModuleSerializer(ModelSerializer):
    question = serializers.SerializerMethodField()

    def get_question(self, obj):
        questions = Question.objects.filter(module=obj)
        question_serializer = QuestionSerializer(questions, many=True)
        return question_serializer.data

    class Meta:
        model = Module
        fields = ['title', 'topic', 'question']




class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['title', 'content']


class TopicSerializer(ModelSerializer):
    lectures = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()

    def get_lectures(self, obj):
        lectures = Lecture.objects.filter(topic=obj)
        lecture_serializer = LectureSerializer(lectures, many=True)
        return lecture_serializer.data

    def get_modules(self, obj):
        modules = Module.objects.filter(topic=obj)
        module_serializer = ModuleSerializer(modules, many=True)
        return module_serializer.data

    class Meta:
        model = Topic
        fields = ['id', 'title', 'link', 'lectures', 'modules']



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
    category_name = serializers.CharField(source='category.name', read_only=True)
    pic = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()

    def get_topics(self, obj):
        topics = Topic.objects.filter(course=obj)
        topic_serializer = TopicSerializer(topics, many=True)
        return topic_serializer.data

    def get_pic(self, obj):
        request = self.context.get('request')
        if obj.pic:
            return request.build_absolute_uri(obj.pic.url)
        return None

    class Meta:
        model = Course
        fields = ['id','title', 'description', 'pic', 'category', 'category_name', 'is_paid', 'amount', 'currency', 'author', 'topics']

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

