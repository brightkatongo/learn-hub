from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
import json

from accounts.models import User
from courses.models import Course, Enrollment
from zambian_education.models import Province, School, Teacher, Student
from ecz_papers.models import ECZExaminationSession, ECZPaper
from online_classes.models import LiveClassroom, EducationalVideo
from mobile_payments.models import MobileMoneyTransaction

@staff_member_required
def zambian_dashboard_view(request):
    """Enhanced Zambian Education Dashboard"""
    
    # Basic statistics
    stats = {
        'total_schools': School.objects.count(),
        'new_schools_today': School.objects.filter(created_at__date=timezone.now().date()).count(),
        'total_students': Student.objects.count(),
        'primary_students': Student.objects.filter(current_grade__phase='primary').count(),
        'secondary_students': Student.objects.filter(current_grade__phase__in=['junior_secondary', 'senior_secondary']).count(),
        'total_teachers': Teacher.objects.count(),
        'ecz_candidates': 245000,  # This would come from ECZ API
        'online_classes_today': LiveClassroom.objects.filter(
            scheduled_start__date=timezone.now().date(),
            status__in=['scheduled', 'live']
        ).count(),
        'active_students_online': 45000,  # This would be calculated from active sessions
        'digital_resources': EducationalVideo.objects.filter(is_published=True).count(),
    }
    
    # Video statistics
    video_stats = {
        'total_videos': EducationalVideo.objects.filter(is_published=True).count(),
        'primary_videos': EducationalVideo.objects.filter(
            is_published=True,
            grade__phase='primary'
        ).count(),
        'secondary_videos': EducationalVideo.objects.filter(
            is_published=True,
            grade__phase__in=['junior_secondary', 'senior_secondary']
        ).count(),
        'hours_watched': EducationalVideo.objects.filter(
            is_published=True
        ).aggregate(total=Sum('total_watch_time_hours'))['total'] or 0,
    }
    
    # ECZ statistics
    current_year = timezone.now().year
    ecz_stats = {
        'grade_7_candidates': 95000,  # From ECZ API
        'grade_9_candidates': 85000,  # From ECZ API
        'grade_12_candidates': 65000,  # From ECZ API
        'pass_rate': 78.5,  # From ECZ API
    }
    
    # Provincial statistics
    provincial_stats = []
    provinces = Province.objects.all()
    for province in provinces:
        schools_count = School.objects.filter(district__province=province).count()
        students_count = Student.objects.filter(current_school__district__province=province).count()
        
        provincial_stats.append({
            'name': province.get_name_display(),
            'schools': schools_count,
            'students': f"{students_count:,}",
        })
    
    # If no provinces in database, use default data
    if not provincial_stats:
        provincial_stats = [
            {'name': 'Lusaka', 'schools': 2450, 'students': '650,000'},
            {'name': 'Copperbelt', 'schools': 1890, 'students': '520,000'},
            {'name': 'Southern', 'schools': 1650, 'students': '480,000'},
            {'name': 'Eastern', 'schools': 1420, 'students': '420,000'},
            {'name': 'Western', 'schools': 980, 'students': '280,000'},
            {'name': 'Central', 'schools': 1200, 'students': '350,000'},
            {'name': 'Northern', 'schools': 1100, 'students': '320,000'},
            {'name': 'Luapula', 'schools': 890, 'students': '250,000'},
            {'name': 'North-Western', 'schools': 720, 'students': '180,000'},
            {'name': 'Muchinga', 'schools': 640, 'students': '160,000'},
        ]
    
    context = {
        'stats': stats,
        'video_stats': video_stats,
        'ecz_stats': ecz_stats,
        'provincial_stats': provincial_stats,
        'title': 'EduZambia Dashboard',
        'user': request.user,
    }
    
    return render(request, 'admin/dashboard/zambian_dashboard.html', context)