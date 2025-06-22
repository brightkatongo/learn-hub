from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import User, UserProfile, InstructorProfile
from .serializers import (
    CustomTokenObtainPairSerializer, UserRegistrationSerializer, 
    UserSerializer, UserProfileSerializer, InstructorProfileSerializer,
    PasswordChangeSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send welcome email
        try:
            send_mail(
                'Welcome to LearnHub!',
                f'Welcome {user.first_name}! Your account has been created successfully.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't fail registration if email fails
            
        return Response(
            {'message': 'User created successfully'}, 
            status=status.HTTP_201_CREATED
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class InstructorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.user_type != 'instructor':
            raise permissions.PermissionDenied("Only instructors can access this endpoint")
        profile, created = InstructorProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ratelimit(key='user', rate='3/m', method='POST')
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        return Response({'message': 'Password changed successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_stats(request):
    user = request.user
    stats = {
        'total_courses': 0,
        'completed_courses': 0,
        'certificates_earned': 0,
        'total_hours': 0,
    }
    
    if user.user_type == 'student':
        from courses.models import Enrollment
        enrollments = Enrollment.objects.filter(user=user)
        stats['total_courses'] = enrollments.count()
        stats['completed_courses'] = enrollments.filter(completed=True).count()
        stats['certificates_earned'] = enrollments.filter(certificate_issued=True).count()
        stats['total_hours'] = sum([e.time_spent for e in enrollments])
    
    elif user.user_type == 'instructor':
        from courses.models import Course
        courses = Course.objects.filter(instructor=user)
        stats['total_courses'] = courses.count()
        stats['total_students'] = sum([c.enrollments.count() for c in courses])
        stats['total_revenue'] = sum([c.total_revenue for c in courses])
        stats['average_rating'] = user.instructor_profile.average_rating if hasattr(user, 'instructor_profile') else 0
    
    return Response(stats)
