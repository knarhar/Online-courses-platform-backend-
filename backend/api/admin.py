from django.contrib import admin
from .models import CourseCategory, Course, Topic, Lecture, Module, Article, Question, Answers, CustomUser, Enrollment, ModuleProgress, LectureProgress, UserProgress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','username', 'email', 'name','pic', 'bank_account', 'is_active', 'is_staff', 'created')


admin.site.register(CustomUser, CustomUserAdmin)

# Model Registration to Admin Panel


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_category', 'is_paid', 'amount', 'currency', 'author', 'pic')

    def display_category(self, obj):
        return obj.category.name
    display_category.short_description = 'Category'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'display_course' ,'enrollment_date')

    def display_course(self, obj):
        return obj.course.title
    display_course.short_description = 'course'

    def display_user(self, obj):
        return obj.user.username
    display_user.short_description = 'user'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'link')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'link','topic')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('module', 'question')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_correct')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'content', 'category', 'pub_date')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'course')

