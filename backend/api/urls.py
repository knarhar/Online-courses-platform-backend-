from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('login/', views.login_view, name='login'),
    path('register/', register_user, name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courses/', views.getCourses, name='courses'),
    path('courses/<str:pk>/', views.getCourse, name='course'),
    path('articles/', views.getArticles, name='articles'),
    path('articles/<str:pk>/', views.getArticle, name='article'),
]


