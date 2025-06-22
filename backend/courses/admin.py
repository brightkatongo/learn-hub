from django.contrib import admin
from .models import Category, Course, Section, Lecture, Enrollment, Review, Quiz, Question

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'status', 'price', 'is_free', 'created_at')
    list_filter = ('status', 'difficulty_level', 'is_free', 'is_bestseller', 'category', 'created_at')
    search_fields = ('title', 'description', 'instructor__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'description', 'instructor', 'category')
        }),
        ('Media', {
            'fields': ('thumbnail', 'preview_video')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'is_free')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'language', 'status', 'requirements', 
                      'what_you_will_learn', 'target_audience')
        }),
        ('Flags', {
            'fields': ('is_bestseller', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('total_duration', 'total_lectures'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'payment_status', 'progress_percentage', 'completed', 'enrolled_at')
    list_filter = ('payment_status', 'completed', 'certificate_issued', 'enrolled_at')
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('id', 'enrolled_at', 'last_accessed')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__email', 'comment')
