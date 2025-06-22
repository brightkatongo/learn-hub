from django.contrib import admin
from .models import UserActivity, CourseAnalytics, LearningPath, PlatformAnalytics

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'course', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('id', 'created_at')

@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('course', 'total_enrollments', 'total_completions', 'conversion_rate', 'completion_rate')
    search_fields = ('course__title',)
    readonly_fields = ('last_updated',)

@admin.register(PlatformAnalytics)
class PlatformAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'new_users', 'active_users', 'new_enrollments', 'daily_revenue')
    list_filter = ('date',)
    ordering = ['-date']
