from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import (
    Category, Course, Section, Lecture, Enrollment, 
    LectureProgress, Review, Quiz, Question
)
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    CourseCreateSerializer, EnrollmentSerializer, LectureProgressSerializer,
    ReviewSerializer, QuizSerializer, SectionSerializer, LectureSerializer
)
from .filters import CourseFilter

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'instructor__first_name', 'instructor__last_name']
    ordering_fields = ['created_at', 'price', 'total_students']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Course.objects.filter(status='published').select_related('instructor', 'category')

class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Course.objects.filter(status='published').select_related('instructor', 'category').prefetch_related('sections__lectures')

class InstructorCourseListView(generics.ListCreateAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseListSerializer

class InstructorCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

class EnrollmentListView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course')

class EnrollmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

class LectureProgressView(generics.RetrieveUpdateAPIView):
    serializer_class = LectureProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        enrollment_id = self.kwargs['enrollment_id']
        lecture_id = self.kwargs['lecture_id']
        
        enrollment = Enrollment.objects.get(id=enrollment_id, user=self.request.user)
        progress, created = LectureProgress.objects.get_or_create(
            enrollment=enrollment,
            lecture_id=lecture_id
        )
        return progress

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id).select_related('user')

class SectionListCreateView(generics.ListCreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id, instructor=self.request.user)
        return Section.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id, instructor=self.request.user)
        serializer.save(course=course)

class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        section_id = self.kwargs['section_id']
        return Lecture.objects.filter(section_id=section_id)
    
    def perform_create(self, serializer):
        section_id = self.kwargs['section_id']
        section = Section.objects.get(id=section_id, course__instructor=self.request.user)
        serializer.save(section=section)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_courses(request):
    courses = Course.objects.filter(
        status='published', 
        is_featured=True
    ).select_related('instructor', 'category')[:6]
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_courses(request):
    courses = Course.objects.filter(
        status='published'
    ).annotate(
        student_count=Count('enrollments')
    ).order_by('-student_count')[:6]
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id, status='published')
        
        # Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            user=request.user,
            course=course,
            amount_paid=course.price if not course.is_free else 0,
            payment_status='completed' if course.is_free else 'pending'
        )
        
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def course_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    level = request.GET.get('level', '')
    price_range = request.GET.get('price_range', '')
    
    courses = Course.objects.filter(status='published')
    
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(instructor__first_name__icontains=query) |
            Q(instructor__last_name__icontains=query)
        )
    
    if category:
        courses = courses.filter(category__slug=category)
    
    if level:
        courses = courses.filter(difficulty_level=level)
    
    if price_range == 'free':
        courses = courses.filter(is_free=True)
    elif price_range == 'paid':
        courses = courses.filter(is_free=False)
    
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)
