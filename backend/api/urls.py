from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('courses/', views.getCourses, name='courses'),
    path('courses/<str:pk>/', views.getCourse, name='course'),
    path('articles/', views.getArticles, name='articles'),
    path('articles/<str:pk>/', views.getArticle, name='article'),
]
