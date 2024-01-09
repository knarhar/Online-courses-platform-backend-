from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Course, Article, CustomUser
from .serializers import CourseSerializer, ArticleSerializer, UserSerializer

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')  # Добавлено поле email

        # Проверка наличия обязательных полей
        if not username or not password or not email:
            return JsonResponse({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка существующего пользователя по имени пользователя и почте
        User = get_user_model()
        try:
            User.objects.get(username=username)
            return JsonResponse({'error': 'User with this username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            return JsonResponse({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        # Создание пользователя
        try:
            new_user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),  # Хеширование пароля
            )
            return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'User creation failed due to integrity error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([SessionAuthentication])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')  # Используйте 'username' вместо 'email'
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def getRoutes(request):
    return Response('Api')


@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def getCourse(request, pk):
    courses = Course.objects.get(id=pk)
    serializer = CourseSerializer(courses, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getArticle(request, pk):
    articles = Article.objects.get(id=pk)
    serializer = ArticleSerializer(articles, many=False)
    return Response(serializer.data)




