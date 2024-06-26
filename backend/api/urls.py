from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, get_courses_by_category, enroll_user, my_courses, get_articles_by_category, update_profile

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('login/', views.login_view, name='login'),
    path('register/', register_user, name='register_user'),
    path('profile/', views.this_user_profile, name="this-user-profile"),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courses/', views.getCourses, name='courses'),
    path('courses/<str:pk>/', views.getCourse, name='course'),
    path('courses/category/<str:category_name>/', get_courses_by_category, name='get_courses_by_category'),
    path('my-courses/', my_courses, name='my-courses'),
    path('courses/<int:course_id>/progress/', views.CourseProgressView.as_view(), name='course_progress'),
    path('courses/<int:course_id>/total_progress/', views.get_total_course_progress, name='course_total_progress'),
    path('courses/<int:course_id>/lectures/<int:lecture_id>/', views.getLecture, name='getLecture'),
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/', views.get_lectures_for_topic, name='get_lectures_for_topic'),
    path('courses/<int:course_id>/topics/<int:topic_id>/lectures/<int:lecture_id>/complete', views.update_lecture_progress, name='upd_lect_progress'),
    path('courses/<int:course_id>/modules/<int:module_id>/', views.getModule, name='getModule'),
    path('courses/<int:course_id>/topics/<int:topic_id>/module/<int:module_id>/complete', views.update_module_progress, name='upd_module_progress'),
    path('course/create/', views.create_course, name='create-course'),
    path('lectures/add/', views.create_lecture, name='add-lecture'),
    path('modules/add/', views.create_module, name='add-module'),

    path('user-progress/<int:user_id>/courses/<int:course_id>/initialize', views.initialize_user_progress, name='initialize_user_progress'),
    path('enrollment/<str:course_id>/', enroll_user, name='enroll_user'),
    path('articles/', views.getArticles, name='articles'),
    path('articles/<str:pk>/', views.getArticle, name='article'),
    path('articles/category/<str:category_name>/', get_articles_by_category, name='get_articles_by_category'),
    path('article/add/', views.addArticle, name='add_article'),
    path('newsletter-subscription/', views.newsletter_subscribing, name='newsletter'),
]

