from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Course, Article, CustomUser, Enrollment, Lecture, Module, UserProgress,  Topic
from .serializers import CourseSerializer, ArticleSerializer, UserSerializer, EnrollmentSerializer, LectureSerializer, ModuleSerializer, UserProgressSerializer
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
        email = data.get('email')
        if not username or not password or not email:
            return JsonResponse({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)


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




@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def this_user_profile(request):
    user = request.user
    user_serializer = UserSerializer(user, context={'request': request})
    context_data = {
        "user": user_serializer.data,
    }

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
def get_lectures_for_topic(request, course_id, topic_id):
    try:
        lectures = Lecture.objects.filter(topic__course_id=course_id, topic_id=topic_id)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def getLecture(request, course_id, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    serializer = LectureSerializer(lecture, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getModule(request, course_id, module_id):
    module = Module.objects.get(id=module_id)
    serializer = ModuleSerializer(module, many=False)
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


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def enroll_user(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        if request.method == 'POST':
            enrollment = Enrollment.objects.create(user=request.user, course=course)
            return Response({'message': 'Enrollment successful'})
        elif request.method == 'DELETE':
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            enrollment.delete()
            return Response({'message': 'Unenrollment successful'})
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Enrollment not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True, context={'request': request})
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
class CourseProgressView(APIView):

    def __init__(self):
        pass

    def get(self, request, course_id):
        user = request.user
        try:
            # Получаем прогресс пользователя по курсу
            user_progress = UserProgress.objects.get(user=user, course_id=course_id)

            # Получаем общее количество лекций и модулей для данного курса
            total_lectures = Lecture.objects.filter(topic__course_id=course_id).count()
            total_modules = Module.objects.filter(topic__course_id=course_id).count()

            # Сериализуем данные о прогрессе пользователя
            serializer = UserProgressSerializer(user_progress)
            user_progress_data = serializer.data

            # Добавляем общее количество лекций и модулей в данные о прогрессе пользователя
            user_progress_data['total_lectures'] = total_lectures
            user_progress_data['total_modules'] = total_modules

            return Response(user_progress_data)
        except UserProgress.DoesNotExist:
            return Response({'error': 'User progress not found for this course'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def initialize_user_progress(request, user_id, course_id):
    # Проверяем, существует ли уже прогресс пользователя для этого курса
    user_progress, created = UserProgress.objects.get_or_create(user_id=user_id, course_id=course_id)

    if created:
        # Если прогресс пользователя только что создан, инициализируем его для первой лекции курса
        user_progress.save()

        return Response({'message': 'User progress initialized successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'User progress already initialized'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_lecture_progress(request, course_id, topic_id, lecture_id):
    user = request.user

    try:
        user_progress, created = UserProgress.objects.get_or_create(
            user=user, course_id=course_id
        )
        user_progress.completed_topics.add(topic_id)
        lecture = Lecture.objects.get(pk=lecture_id)

        user_progress.completed_lectures.add(lecture)
        user_progress.save()

        return Response({'message': 'Lecture completed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_module_progress(request, course_id, topic_id, module_id):
    user = request.user
    module = Module.objects.get(pk=module_id)
    quiz_results = request.data.get('quiz_results')
    try:
        user_progress = UserProgress.objects.get(user=user, course_id=course_id)
        user_progress.completed_topics.add(topic_id)
        user_progress.completed_modules.add(module)
        user_progress.quiz_results += quiz_results
        user_progress.quiz_completitions += 1
        user_progress.save()
        return Response({'message': 'Quiz completed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_total_course_progress(request, course_id):
    user = request.user
    try:
        user_progress = UserProgress.objects.get(user=user, course_id=course_id)
        course = user_progress.course
        average_quiz_score = user_progress.calculate_average_quiz_score(course)
        return Response({'average_quiz_score': average_quiz_score}, status=status.HTTP_200_OK)
    except UserProgress.DoesNotExist:
        return Response({'error': 'User progress for this course does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)