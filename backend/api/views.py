from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Course, Article, CustomUser, Enrollment
from .serializers import CourseSerializer, ArticleSerializer, UserSerializer, EnrollmentSerializer
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

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
                password=make_password(password),
            )
            return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'error': 'User creation failed due to integrity error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.



@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Аутентификация прошла успешно

            # Генерация токенов доступа и обновления
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Возвращаем токены в ответе
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            # Неверные учетные данные
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def this_user_profile(request):
    user = request.user  # This will give you the user associated with the access token

    user_serializer = UserSerializer(user, context={'request': request})

    context_data = {
        "user": user_serializer.data,
    }

    # Do additional logic based on the user if needed

    return Response(context_data, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@permission_classes([IsAuthenticated])
def profile(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserSerializer(user, context={'request': request})

    context_data = {
        "auth": False,
    }

    if request.user == user:
        context_data['user'] = user_serializer.data
        context_data["auth"] = True

    return Response(context_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user_profile = CustomUser.objects.get(id=request.user.id)

    serializer = UserSerializer(user_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    return Response('Api')


@api_view(['GET'])
def getCourses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@permission_classes([IsAuthenticated])
def getCourse(request, pk):
    courses = get_object_or_404(Course.objects.prefetch_related('topic_set'), id=pk)
    serializer = CourseSerializer(courses, context={'request': request}, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_courses_by_category(request, category_name):
    courses = Course.objects.filter(category=category_name)
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def getArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_articles_by_category(request, category_name):
    articles = Article.objects.filter(category=category_name)
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def getArticle(request, pk):
    articles = Article.objects.get(id=pk)
    serializer = ArticleSerializer(articles, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_user(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        enrollment = Enrollment.objects.create(user=request.user, course=course)
        return Response({'message': 'Enrollment successful'})
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_enrollment_status(request, course_id):
#     try:
#         course = Course.objects.get(pk=course_id)
#         enrollment = Enrollment.objects.get(user=request.user, course=course)
#         serializer = EnrollmentSerializer(enrollment)
#         return Response({'status': 'Enrolled', 'enrollment_data': serializer.data})
#     except Enrollment.DoesNotExist:
#         return Response({'status': 'Not Enrolled'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True, context={'request': request})
    return Response(serializer.data)