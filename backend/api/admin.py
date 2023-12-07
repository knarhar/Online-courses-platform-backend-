from django.contrib import admin
from .models import CourseCategory, Course, Topic, Lecture, Module, Article, Question, Answers, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'name','pic', 'bank_account', 'is_active', 'is_staff', 'created')


admin.site.register(CustomUser, CustomUserAdmin)

# Model Registration to Admin Panel


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'display_category', 'is_paid', 'amount', 'currency', 'author')

    def display_category(self, obj):
        return obj.category.name
    display_category.short_description = 'Category'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'link')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'topic')


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
