from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Article, CustomUser, Topic, Lecture, Answers, Question, Module, Enrollment, UserProgress


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
        fields = ['id', 'question', 'answer']


class ModuleSerializer(ModelSerializer):
    question = serializers.SerializerMethodField()

    def get_question(self, obj):
        questions = Question.objects.filter(module=obj)
        question_serializer = QuestionSerializer(questions, many=True)
        return question_serializer.data

    class Meta:
        model = Module
        fields = ['id', 'title', 'topic', 'question']


class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'content', 'link', 'topic']

    def create(self, validated_data):
        topic_data = validated_data.pop('topic', None)
        if topic_data:
            topic_instance, _ = Topic.objects.get_or_create(title=topic_data)
            validated_data['topic'] = topic_instance

        lecture = Lecture.objects.create(**validated_data)
        return lecture


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
    is_enrolled = serializers.SerializerMethodField()

    def get_topics(self, obj):
        topics = Topic.objects.filter(course=obj)
        topic_serializer = TopicSerializer(topics, many=True)
        return topic_serializer.data

    def get_pic(self, obj):
        request = self.context.get('request')
        if obj.pic:
            return request.build_absolute_uri(obj.pic.url)
        return None

    def get_is_enrolled(self, obj):
        request = self.context.get('request')

        try:
            user = CustomUser.objects.get(pk=request.user.id)
            if user.is_authenticated:
                return Enrollment.objects.filter(user=user, course=obj).exists()
        except CustomUser.DoesNotExist:
            return False
        return False

    class Meta:
        model = Course
        fields = ['id','title', 'description', 'pic', 'category', 'category_name', 'is_paid', 'amount', 'currency', 'author', 'topics', 'is_enrolled']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Assuming you have a CourseSerializer defined

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrollment_date']


class ArticleSerializer(ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'



class UserProgressSerializer(serializers.ModelSerializer):
    completed_topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    completed_modules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    completed_lectures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = UserProgress
        fields = '__all__'

