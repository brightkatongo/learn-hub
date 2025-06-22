from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lecture
import uuid

User = get_user_model()

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('course_view', 'Course View'),
        ('course_enroll', 'Course Enroll'),
        ('lecture_start', 'Lecture Start'),
        ('lecture_complete', 'Lecture Complete'),
        ('quiz_attempt', 'Quiz Attempt'),
        ('certificate_earn', 'Certificate Earn'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, blank=True, null=True)
    
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['course', 'activity_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type} - {self.created_at}"

class CourseAnalytics(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='analytics')
    
    total_views = models.PositiveIntegerField(default=0)
    total_enrollments = models.PositiveIntegerField(default=0)
    total_completions = models.PositiveIntegerField(default=0)
    
    average_completion_time = models.PositiveIntegerField(default=0)  # in minutes
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # views to enrollments
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # enrollments to completions
    
    revenue_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    revenue_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.course.title}"

class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    courses = models.ManyToManyField(Course, through='LearningPathCourse')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"

class LearningPathCourse(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['learning_path', 'course']

class PlatformAnalytics(models.Model):
    date = models.DateField(unique=True)
    
    total_users = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    
    total_courses = models.PositiveIntegerField(default=0)
    new_courses = models.PositiveIntegerField(default=0)
    
    total_enrollments = models.PositiveIntegerField(default=0)
    new_enrollments = models.PositiveIntegerField(default=0)
    
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    daily_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Platform Analytics - {self.date}"
