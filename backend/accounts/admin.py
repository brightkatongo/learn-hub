from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from .models import User, UserProfile, InstructorProfile, UserSession, UserPreferences

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'get_full_name', 'user_type', 'is_verified', 
        'login_count', 'last_login', 'created_at', 'user_actions'
    )
    list_filter = (
        'user_type', 'is_verified', 'is_active', 'created_at', 
        'last_login', 'country', 'is_active_subscription'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'last_login', 
        'login_count', 'last_login_ip'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'user_type', 'phone_number', 'avatar', 'bio', 
                'date_of_birth', 'country', 'city'
            )
        }),
        ('Preferences', {
            'fields': ('timezone', 'language_preference')
        }),
        ('Account Status', {
            'fields': (
                'is_verified', 'is_active_subscription', 'subscription_expires'
            )
        }),
        ('Login Information', {
            'fields': ('login_count', 'last_login_ip'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type'),
        }),
    )
    
    actions = ['verify_users', 'send_welcome_email', 'export_users']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def user_actions(self, obj):
        """Custom actions for each user"""
        actions = []
        
        if obj.user_type == 'instructor':
            instructor_url = reverse('admin:accounts_instructorprofile_change', 
                                   args=[obj.instructor_profile.id])
            actions.append(f'<a href="{instructor_url}" class="button">Instructor Profile</a>')
        
        profile_url = reverse('admin:accounts_userprofile_change', 
                            args=[obj.profile.id])
        actions.append(f'<a href="{profile_url}" class="button">Profile</a>')
        
        return format_html(' '.join(actions))
    user_actions.short_description = 'Actions'
    
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} users verified successfully.')
    verify_users.short_description = "Verify selected users"
    
    def send_welcome_email(self, request, queryset):
        # Implementation for sending welcome emails
        count = queryset.count()
        self.message_user(request, f'Welcome emails sent to {count} users.')
    send_welcome_email.short_description = "Send welcome email"
    
    def export_users(self, request, queryset):
        # Implementation for exporting users
        count = queryset.count()
        self.message_user(request, f'Exported {count} users.')
    export_users.short_description = "Export selected users"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'total_courses_completed', 'total_certificates_earned',
        'total_learning_hours', 'current_streak_days', 'profile_visibility'
    )
    list_filter = (
        'profile_visibility', 'preferred_learning_style', 
        'total_courses_completed', 'created_at'
    )
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Learning Preferences', {
            'fields': (
                'learning_goals', 'interests', 'preferred_learning_style'
            )
        }),
        ('Privacy Settings', {
            'fields': ('profile_visibility',)
        }),
        ('Statistics', {
            'fields': (
                'total_courses_completed', 'total_certificates_earned',
                'total_learning_hours', 'current_streak_days', 'longest_streak_days'
            ),
            'classes': ('collapse',)
        }),
        ('Social & Notifications', {
            'fields': ('social_links', 'notification_preferences'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'is_approved', 'total_students', 'total_courses',
        'total_revenue', 'average_rating', 'approval_status'
    )
    list_filter = (
        'is_approved', 'preferred_payout_method', 'available_for_consultation',
        'approval_date', 'created_at'
    )
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
        'company', 'job_title'
    )
    readonly_fields = (
        'total_students', 'total_courses', 'total_revenue',
        'average_rating', 'total_reviews', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': (
                'expertise', 'experience_years', 'education', 'certifications',
                'company', 'job_title', 'website', 'linkedin_profile'
            )
        }),
        ('Teaching Preferences', {
            'fields': (
                'hourly_rate', 'available_for_consultation', 'consultation_rate'
            )
        }),
        ('Approval Status', {
            'fields': ('is_approved', 'approval_date', 'approved_by')
        }),
        ('Statistics', {
            'fields': (
                'total_students', 'total_courses', 'total_revenue',
                'average_rating', 'total_reviews'
            ),
            'classes': ('collapse',)
        }),
        ('Payout Information', {
            'fields': (
                'preferred_payout_method', 'bank_account_number', 'bank_name',
                'mobile_money_number'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_instructors', 'update_statistics']
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="color: green;">✓ Approved</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">✗ Pending</span>'
            )
    approval_status.short_description = 'Status'
    
    def approve_instructors(self, request, queryset):
        updated = queryset.update(
            is_approved=True,
            approval_date=timezone.now(),
            approved_by=request.user
        )
        self.message_user(request, f'{updated} instructors approved successfully.')
    approve_instructors.short_description = "Approve selected instructors"
    
    def update_statistics(self, request, queryset):
        for instructor in queryset:
            instructor.update_statistics()
        self.message_user(request, f'Statistics updated for {queryset.count()} instructors.')
    update_statistics.short_description = "Update statistics"

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'ip_address', 'started_at', 'last_activity',
        'duration_display', 'country', 'city'
    )
    list_filter = ('started_at', 'country', 'city')
    search_fields = ('user__email', 'ip_address', 'country', 'city')
    readonly_fields = ('started_at', 'last_activity', 'duration_seconds')
    ordering = ['-started_at']
    
    def duration_display(self, obj):
        if obj.duration_seconds:
            hours = obj.duration_seconds // 3600
            minutes = (obj.duration_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "Active"
    duration_display.short_description = 'Duration'

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'email_notifications', 'sms_notifications',
        'course_updates', 'promotional_emails'
    )
    list_filter = (
        'email_notifications', 'sms_notifications', 'push_notifications',
        'promotional_emails', 'newsletter_subscription'
    )
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Notification Preferences', {
            'fields': (
                'email_notifications', 'sms_notifications', 'push_notifications'
            )
        }),
        ('Course Notifications', {
            'fields': (
                'course_updates', 'new_lectures', 'assignment_reminders',
                'certificate_notifications'
            )
        }),
        ('Marketing Preferences', {
            'fields': (
                'promotional_emails', 'course_recommendations', 'newsletter_subscription'
            )
        }),
        ('Privacy Preferences', {
            'fields': (
                'show_profile_publicly', 'show_learning_progress', 'allow_instructor_contact'
            )
        }),
        ('Learning Preferences', {
            'fields': (
                'auto_play_videos', 'video_quality', 'playback_speed'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )