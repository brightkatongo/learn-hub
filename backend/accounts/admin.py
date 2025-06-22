from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, InstructorProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number', 'avatar', 'bio', 'date_of_birth', 'is_verified')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'language_preference')
    search_fields = ('user__email', 'user__username')

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'is_approved', 'total_students', 'average_rating')
    list_filter = ('is_approved', 'experience_years')
    search_fields = ('user__email', 'user__username')
    actions = ['approve_instructors']
    
    def approve_instructors(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_approved=True, approval_date=timezone.now())
    approve_instructors.short_description = "Approve selected instructors"
