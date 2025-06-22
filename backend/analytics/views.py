from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from .models import UserActivity, CourseAnalytics, LearningPath, PlatformAnalytics
from .serializers import UserActivitySerializer, CourseAnalyticsSerializer, LearningPathSerializer
from courses.models import Course, Enrollment

class UserActivityListView(generics.ListAPIView):
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def track_activity(request):
    activity_type = request.data.get('activity_type')
    course_id = request.data.get('course_id')
    lecture_id = request.data.get('lecture_id')
    metadata = request.data.get('metadata', {})
    
    activity = UserActivity.objects.create(
        user=request.user,
        activity_type=activity_type,
        course_id=course_id,
        lecture_id=lecture_id,
        metadata=metadata,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    serializer = UserActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_learning_stats(request):
    user = request.user
    
    # Get user's enrollments
    enrollments = Enrollment.objects.filter(user=user)
    
    # Calculate stats
    stats = {
        'total_courses': enrollments.count(),
        'completed_courses': enrollments.filter(completed=True).count(),
        'in_progress_courses': enrollments.filter(completed=False, progress_percentage__gt=0).count(),
        'certificates_earned': enrollments.filter(certificate_issued=True).count(),
        'total_time_spent': sum([e.time_spent for e in enrollments]),
        'average_progress': enrollments.aggregate(avg_progress=Avg('progress_percentage'))['avg_progress'] or 0,
    }
    
    # Learning streak
    activities = UserActivity.objects.filter(
        user=user,
        activity_type__in=['lecture_start', 'lecture_complete']
    ).order_by('-created_at')
    
    current_streak = 0
    if activities.exists():
        current_date = timezone.now().date()
        for activity in activities:
            if activity.created_at.date() == current_date:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
    
    stats['current_streak'] = current_streak
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def instructor_analytics(request):
    if request.user.user_type != 'instructor':
        return Response(
            {'error': 'Only instructors can access this endpoint'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    courses = Course.objects.filter(instructor=request.user)
    
    # Calculate instructor stats
    stats = {
        'total_courses': courses.count(),
        'published_courses': courses.filter(status='published').count(),
        'draft_courses': courses.filter(status='draft').count(),
        'total_students': sum([course.total_students for course in courses]),
        'total_revenue': sum([course.total_revenue for course in courses]),
        'average_rating': courses.aggregate(avg_rating=Avg('reviews__rating'))['avg_rating'] or 0,
    }
    
    # Monthly stats
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_enrollments = Enrollment.objects.filter(
        course__in=courses,
        enrolled_at__gte=thirty_days_ago
    )
    
    stats['monthly_enrollments'] = recent_enrollments.count()
    stats['monthly_revenue'] = sum([e.amount_paid for e in recent_enrollments])
    
    # Course performance
    course_stats = []
    for course in courses.filter(status='published'):
        course_analytics, created = CourseAnalytics.objects.get_or_create(course=course)
        course_stats.append({
            'course_id': course.id,
            'course_title': course.title,
            'total_students': course.total_students,
            'total_revenue': course.total_revenue,
            'average_rating': course.average_rating,
            'completion_rate': course_analytics.completion_rate,
        })
    
    stats['course_performance'] = course_stats
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def platform_analytics(request):
    # Get date range from query params
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get platform analytics for the date range
    analytics = PlatformAnalytics.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # Calculate totals
    from accounts.models import User
    from courses.models import Course
    from payments.models import Payment
    
    total_stats = {
        'total_users': User.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_revenue': Payment.objects.filter(payment_status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }
    
    # Daily analytics
    daily_stats = []
    for analytic in analytics:
        daily_stats.append({
            'date': analytic.date,
            'new_users': analytic.new_users,
            'active_users': analytic.active_users,
            'new_enrollments': analytic.new_enrollments,
            'daily_revenue': analytic.daily_revenue,
        })
    
    return Response({
        'total_stats': total_stats,
        'daily_stats': daily_stats,
        'date_range': {
            'start_date': start_date,
            'end_date': end_date,
        }
    })

class LearningPathListCreateView(generics.ListCreateAPIView):
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LearningPathDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)
