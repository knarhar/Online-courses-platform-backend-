from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import json

# Create your models here.

def user_pic_path(instance, filename):
    return os.path.join('user_pic', str(instance.id), filename)


def course_pic_path(instance, filename):
    return os.path.join('course_pic', str(instance.id), filename)


# Courses and Articles category model
class CourseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Model for users
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(blank=True, null=True, max_length=50)
    bio = models.TextField(blank=True, null=True, max_length=255)

    pic = models.ImageField(upload_to=user_pic_path, default='avatar.svg', null=True)
    bank_account = models.CharField(max_length=16, default='0000000000000000')
    created = models.DateTimeField(auto_now_add=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


# Course model
class Course(models.Model):

    currency_choices = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    pic = models.ImageField(upload_to=course_pic_path, default='course.png', null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    currency = models.CharField(max_length=3, choices=currency_choices, default='USD')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title



# Topics model
class Topic(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.title


# Lectures model
class Lecture(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.CharField(max_length=255, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Modules model
class Module(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Question model
class Question(models.Model):
    question = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


# Answers model
class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.answer}  {self.is_correct}'


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_topics = models.ManyToManyField(Topic, related_name='completed_topic_progress', blank=True)
    completed_modules = models.ManyToManyField(Module, related_name='completed_module_progress', blank=True)
    completed_lectures = models.ManyToManyField(Lecture, related_name='completed_lecture_progress', blank=True)
    quiz_results = models.IntegerField(default=0)
    quiz_completitions = models.IntegerField(default=0)

    def set_quiz_results(self, results):
        self.quiz_results = json.dumps(results)

    def get_quiz_results(self):
        return json.loads(self.quiz_results) if self.quiz_results else []

    def __str__(self):
        return f"Progress for User {self.user} in Course {self.course}"

    def calculate_average_quiz_score(self, course):
        if self.quiz_completitions == 0:
            return 0
        average_quiz_score = self.quiz_results / self.quiz_completitions
        return average_quiz_score


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=800, default='')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'



class NewsLetter(models.Model):
    email = models.EmailField()
    subscribing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} subscribed {self.subscribing_date}'
