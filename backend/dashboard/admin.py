from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta, date
import json

from .models import DashboardWidget, SystemMetrics, UserActivity
from accounts.models import User
from courses.models import Course, Enrollment
from payments.models import Payment
from mobile_payments.models import MobileMoneyTransaction

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'widget_type', 'order', 'is_active', 'created_at')
    list_filter = ('widget_type', 'is_active', 'created_at')
    search_fields = ('name', 'title', 'description')
    ordering = ['order', 'name']

@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'total_users', 'new_users_today', 'total_courses', 
        'new_enrollments_today', 'revenue_today'
    )
    list_filter = ('date',)
    ordering = ['-date']
    readonly_fields = ('created_at',)
    
    actions = ['recalculate_metrics']
    
    def recalculate_metrics(self, request, queryset):
        for metric in queryset:
            metric.calculate_metrics()
        self.message_user(request, f'Recalculated metrics for {queryset.count()} days.')
    recalculate_metrics.short_description = "Recalculate selected metrics"

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'action', 'description')
    readonly_fields = ('timestamp',)
    ordering = ['-timestamp']

class DashboardAdminMixin:
    """Mixin to add dashboard functionality to admin"""
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='dashboard'),
            path('analytics/', self.admin_site.admin_view(self.analytics_view), name='analytics'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Main dashboard view with charts and metrics"""
        context = self.get_dashboard_context(request)
        return render(request, 'admin/dashboard/dashboard.html', context)
    
    def analytics_view(self, request):
        """Detailed analytics view"""
        context = self.get_analytics_context(request)
        return render(request, 'admin/dashboard/analytics.html', context)
    
    def get_dashboard_context(self, request):
        """Get context data for dashboard"""
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        
        # Get or create today's metrics
        today_metrics = SystemMetrics.get_or_create_today()
        
        # User statistics
        total_users = User.objects.count()
        new_users_today = User.objects.filter(created_at__date=today).count()
        active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=7)).count()
        
        # Course statistics
        total_courses = Course.objects.count()
        published_courses = Course.objects.filter(status='published').count()
        draft_courses = Course.objects.filter(status='draft').count()
        
        # Enrollment statistics
        total_enrollments = Enrollment.objects.count()
        new_enrollments_today = Enrollment.objects.filter(enrolled_at__date=today).count()
        completed_today = Enrollment.objects.filter(completed=True, completed_at__date=today).count()
        
        # Revenue statistics
        total_revenue = Payment.objects.filter(payment_status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        revenue_today = Payment.objects.filter(
            payment_status='completed',
            completed_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Mobile money statistics
        mobile_payments_today = MobileMoneyTransaction.objects.filter(
            status='confirmed',
            confirmed_at__date=today
        ).count()
        
        mobile_revenue_today = MobileMoneyTransaction.objects.filter(
            status='confirmed',
            confirmed_at__date=today
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Chart data for last 30 days
        daily_metrics = SystemMetrics.objects.filter(
            date__gte=last_30_days
        ).order_by('date')
        
        chart_data = {
            'dates': [m.date.strftime('%Y-%m-%d') for m in daily_metrics],
            'new_users': [m.new_users_today for m in daily_metrics],
            'new_enrollments': [m.new_enrollments_today for m in daily_metrics],
            'revenue': [float(m.revenue_today) for m in daily_metrics],
            'mobile_revenue': [float(m.mobile_revenue_today) for m in daily_metrics],
        }
        
        # User type distribution
        user_types = User.objects.values('user_type').annotate(count=Count('id'))
        user_type_data = {
            'labels': [ut['user_type'].title() for ut in user_types],
            'data': [ut['count'] for ut in user_types]
        }
        
        # Course category distribution
        course_categories = Course.objects.filter(status='published').values(
            'category__name'
        ).annotate(count=Count('id'))
        
        category_data = {
            'labels': [cc['category__name'] for cc in course_categories],
            'data': [cc['count'] for cc in course_categories]
        }
        
        # Recent activities
        recent_activities = UserActivity.objects.select_related('user')[:10]
        
        return {
            'title': 'Dashboard',
            'user': request.user,
            'today_metrics': today_metrics,
            'stats': {
                'total_users': total_users,
                'new_users_today': new_users_today,
                'active_users': active_users,
                'total_courses': total_courses,
                'published_courses': published_courses,
                'draft_courses': draft_courses,
                'total_enrollments': total_enrollments,
                'new_enrollments_today': new_enrollments_today,
                'completed_today': completed_today,
                'total_revenue': total_revenue,
                'revenue_today': revenue_today,
                'mobile_payments_today': mobile_payments_today,
                'mobile_revenue_today': mobile_revenue_today,
            },
            'chart_data': json.dumps(chart_data),
            'user_type_data': json.dumps(user_type_data),
            'category_data': json.dumps(category_data),
            'recent_activities': recent_activities,
        }
    
    def get_analytics_context(self, request):
        """Get context data for analytics page"""
        # Implementation for detailed analytics
        return {
            'title': 'Analytics',
            'user': request.user,
        }

# Apply the mixin to the admin site
from django.contrib.admin import AdminSite

class LearnHubAdminSite(AdminSite, DashboardAdminMixin):
    site_header = 'LearnHub Administration'
    site_title = 'LearnHub Admin'
    index_title = 'Welcome to LearnHub Administration'
    
    def index(self, request, extra_context=None):
        """Override the default admin index to show dashboard"""
        if request.user.is_authenticated:
            return self.dashboard_view(request)
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = LearnHubAdminSite(name='learnhub_admin')

# Register all models with the custom admin site
from django.apps import apps

def auto_register_models():
    """Auto-register all models with the custom admin site"""
    for model in apps.get_models():
        try:
            admin_site.register(model)
        except admin.sites.AlreadyRegistered:
            pass

# Call auto-registration
auto_register_models()