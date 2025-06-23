from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import uuid

User = get_user_model()

class DashboardWidget(models.Model):
    """Model to store custom dashboard widgets"""
    WIDGET_TYPES = [
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('progress', 'Progress'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Widget configuration
    config = models.JSONField(default=dict)
    
    # Display settings
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Permissions
    allowed_roles = models.JSONField(default=list)  # ['admin', 'instructor', 'student']
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.title

class SystemMetrics(models.Model):
    """Model to store system metrics for dashboard"""
    date = models.DateField(unique=True)
    
    # User metrics
    total_users = models.PositiveIntegerField(default=0)
    new_users_today = models.PositiveIntegerField(default=0)
    active_users_today = models.PositiveIntegerField(default=0)
    
    # Course metrics
    total_courses = models.PositiveIntegerField(default=0)
    new_courses_today = models.PositiveIntegerField(default=0)
    published_courses = models.PositiveIntegerField(default=0)
    
    # Enrollment metrics
    total_enrollments = models.PositiveIntegerField(default=0)
    new_enrollments_today = models.PositiveIntegerField(default=0)
    completed_courses_today = models.PositiveIntegerField(default=0)
    
    # Revenue metrics
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue_today = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Mobile money metrics
    mobile_payments_today = models.PositiveIntegerField(default=0)
    mobile_revenue_today = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"
    
    @classmethod
    def get_or_create_today(cls):
        """Get or create metrics for today"""
        today = timezone.now().date()
        metrics, created = cls.objects.get_or_create(date=today)
        
        if created:
            metrics.calculate_metrics()
        
        return metrics
    
    def calculate_metrics(self):
        """Calculate all metrics for this date"""
        from accounts.models import User
        from courses.models import Course, Enrollment
        from payments.models import Payment
        from mobile_payments.models import MobileMoneyTransaction
        
        # User metrics
        self.total_users = User.objects.count()
        self.new_users_today = User.objects.filter(created_at__date=self.date).count()
        self.active_users_today = User.objects.filter(last_login__date=self.date).count()
        
        # Course metrics
        self.total_courses = Course.objects.count()
        self.new_courses_today = Course.objects.filter(created_at__date=self.date).count()
        self.published_courses = Course.objects.filter(status='published').count()
        
        # Enrollment metrics
        self.total_enrollments = Enrollment.objects.count()
        self.new_enrollments_today = Enrollment.objects.filter(enrolled_at__date=self.date).count()
        self.completed_courses_today = Enrollment.objects.filter(
            completed=True, 
            completed_at__date=self.date
        ).count()
        
        # Revenue metrics
        total_payments = Payment.objects.filter(payment_status='completed')
        self.total_revenue = sum(p.amount for p in total_payments)
        
        today_payments = total_payments.filter(completed_at__date=self.date)
        self.revenue_today = sum(p.amount for p in today_payments)
        
        # Mobile money metrics
        mobile_transactions = MobileMoneyTransaction.objects.filter(
            status='confirmed',
            confirmed_at__date=self.date
        )
        self.mobile_payments_today = mobile_transactions.count()
        self.mobile_revenue_today = sum(t.amount for t in mobile_transactions)
        
        self.save()

class UserActivity(models.Model):
    """Track user activity for analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_activities')
    action = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"