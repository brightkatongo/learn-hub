from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import (
    LiveClassroom, ClassEnrollment, ClassSchedule, StudyGroup,
    DigitalResource, VirtualLab, OnlineAssessment, EducationalVideo, VideoWatchHistory
)

@admin.register(EducationalVideo)
class EducationalVideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'grade', 'video_type', 'duration_formatted',
        'quality', 'view_count', 'average_rating', 'is_published', 'is_featured'
    )
    list_filter = (
        'video_type', 'quality', 'subject__category', 'grade__level',
        'is_published', 'is_featured', 'is_free', 'language'
    )
    search_fields = ('title', 'description', 'topic', 'tags', 'keywords')
    readonly_fields = (
        'id', 'view_count', 'like_count', 'average_rating',
        'total_watch_time_hours', 'created_at', 'updated_at'
    )
    filter_horizontal = []
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'description', 'subject', 'grade', 'topic')
        }),
        ('Video Details', {
            'fields': ('video_type', 'duration_seconds', 'quality')
        }),
        ('Files and Media', {
            'fields': ('video_file', 'video_url', 'thumbnail', 'subtitles_file')
        }),
        ('Metadata', {
            'fields': ('file_size_mb', 'language', 'has_subtitles')
        }),
        ('Educational Content', {
            'fields': ('learning_objectives', 'curriculum_alignment', 'prerequisites')
        }),
        ('Creator and Approval', {
            'fields': ('created_by', 'approved_by')
        }),
        ('SEO and Discovery', {
            'fields': ('tags', 'keywords')
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count', 'average_rating', 'total_watch_time_hours'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured', 'is_free')
        })
    )
    
    actions = ['publish_videos', 'unpublish_videos', 'feature_videos']
    
    def publish_videos(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} videos published successfully.')
    publish_videos.short_description = "Publish selected videos"
    
    def unpublish_videos(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} videos unpublished.')
    unpublish_videos.short_description = "Unpublish selected videos"
    
    def feature_videos(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} videos featured.')
    feature_videos.short_description = "Feature selected videos"

@admin.register(VideoWatchHistory)
class VideoWatchHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'video_title', 'completion_percentage', 'watch_time_formatted',
        'total_sessions', 'rating', 'last_watched'
    )
    list_filter = (
        'is_completed', 'liked', 'rating', 'video__subject',
        'video__grade', 'last_watched'
    )
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email',
        'video__title'
    )
    readonly_fields = ('first_watched', 'last_watched')
    
    def video_title(self, obj):
        return obj.video.title[:50]
    video_title.short_description = 'Video'
    
    def watch_time_formatted(self, obj):
        hours = obj.watch_time_seconds // 3600
        minutes = (obj.watch_time_seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    watch_time_formatted.short_description = 'Watch Time'

@admin.register(LiveClassroom)
class LiveClassroomAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'grade', 'teacher', 'class_type',
        'scheduled_start', 'status', 'enrolled_count', 'peak_attendance'
    )
    list_filter = (
        'class_type', 'status', 'subject__category', 'grade__level',
        'meeting_platform', 'is_recorded'
    )
    search_fields = ('title', 'topic', 'teacher__user__first_name', 'teacher__user__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'peak_attendance')
    filter_horizontal = ('enrolled_students',)
    
    fieldsets = (
        ('Class Information', {
            'fields': ('title', 'description', 'subject', 'grade', 'teacher')
        }),
        ('Class Details', {
            'fields': ('class_type', 'topic', 'learning_objectives')
        }),
        ('Scheduling', {
            'fields': (
                'scheduled_start', 'scheduled_end', 'actual_start', 'actual_end'
            )
        }),
        ('Capacity and Enrollment', {
            'fields': ('max_students', 'enrolled_students')
        }),
        ('Technology', {
            'fields': (
                'meeting_platform', 'meeting_id', 'meeting_password', 'meeting_url'
            )
        }),
        ('Content', {
            'fields': ('presentation_slides', 'additional_resources')
        }),
        ('Recording', {
            'fields': ('is_recorded', 'recording_url', 'recording_file')
        }),
        ('Status and Analytics', {
            'fields': ('status', 'peak_attendance', 'average_attendance_duration')
        })
    )
    
    def enrolled_count(self, obj):
        return obj.enrolled_students.count()
    enrolled_count.short_description = 'Enrolled'

@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'classroom', 'enrolled_at', 'attended',
        'attendance_duration', 'questions_asked', 'rating'
    )
    list_filter = (
        'attended', 'rating', 'classroom__subject', 'classroom__grade'
    )
    search_fields = (
        'student__user__first_name', 'student__user__last_name',
        'classroom__title'
    )
    readonly_fields = ('enrolled_at',)

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 'grade', 'teacher', 'day_of_week',
        'time_range', 'is_recurring', 'is_active'
    )
    list_filter = (
        'day_of_week', 'subject__category', 'grade__level',
        'is_recurring', 'is_active'
    )
    search_fields = ('subject__name', 'teacher__user__first_name', 'teacher__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def time_range(self, obj):
        return f"{obj.start_time} - {obj.end_time}"
    time_range.short_description = 'Time'

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'subject', 'grade', 'creator', 'member_count',
        'is_public', 'is_active'
    )
    list_filter = (
        'subject__category', 'grade__level', 'is_public',
        'requires_approval', 'is_active'
    )
    search_fields = ('name', 'description', 'creator__user__first_name')
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(DigitalResource)
class DigitalResourceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'grade', 'resource_type', 'access_level',
        'created_by', 'view_count', 'average_rating', 'is_published'
    )
    list_filter = (
        'resource_type', 'access_level', 'subject__category',
        'grade__level', 'is_published', 'is_featured'
    )
    search_fields = ('title', 'description', 'topic', 'created_by__first_name')
    readonly_fields = (
        'id', 'view_count', 'download_count', 'average_rating',
        'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('title', 'description', 'subject', 'grade', 'topic')
        }),
        ('Resource Details', {
            'fields': ('resource_type', 'access_level')
        }),
        ('Files and URLs', {
            'fields': ('file', 'external_url', 'thumbnail')
        }),
        ('Metadata', {
            'fields': ('duration_minutes', 'file_size_mb', 'language')
        }),
        ('Educational Alignment', {
            'fields': ('curriculum_alignment', 'learning_objectives')
        }),
        ('Quality and Approval', {
            'fields': ('created_by', 'approved_by')
        }),
        ('Statistics', {
            'fields': ('view_count', 'download_count', 'average_rating')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        })
    )

@admin.register(VirtualLab)
class VirtualLabAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'subject', 'lab_type', 'is_free',
        'requires_supervision', 'total_sessions', 'is_active'
    )
    list_filter = (
        'lab_type', 'subject__category', 'is_free',
        'requires_supervision', 'is_active'
    )
    search_fields = ('name', 'description', 'subject__name')
    filter_horizontal = ('applicable_grades',)
    readonly_fields = ('total_sessions', 'average_session_duration', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Lab Information', {
            'fields': ('name', 'description', 'subject', 'applicable_grades')
        }),
        ('Lab Details', {
            'fields': ('lab_type',)
        }),
        ('Technology', {
            'fields': ('simulation_url', 'requires_plugin', 'plugin_requirements')
        }),
        ('Educational Content', {
            'fields': ('experiments', 'learning_outcomes', 'safety_guidelines')
        }),
        ('Access', {
            'fields': ('is_free', 'requires_supervision')
        }),
        ('Usage Statistics', {
            'fields': ('total_sessions', 'average_session_duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

@admin.register(OnlineAssessment)
class OnlineAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'grade', 'teacher', 'assessment_type',
        'total_marks', 'duration_minutes', 'assigned_count', 'is_published'
    )
    list_filter = (
        'assessment_type', 'subject__category', 'grade__level',
        'is_published', 'show_results_immediately'
    )
    search_fields = ('title', 'description', 'teacher__user__first_name')
    filter_horizontal = ('assigned_students',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('title', 'description', 'subject', 'grade', 'teacher')
        }),
        ('Assessment Configuration', {
            'fields': ('assessment_type', 'total_marks', 'duration_minutes')
        }),
        ('Questions', {
            'fields': ('questions',)
        }),
        ('Timing', {
            'fields': ('available_from', 'available_until')
        }),
        ('Settings', {
            'fields': (
                'attempts_allowed', 'show_results_immediately', 'randomize_questions'
            )
        }),
        ('Access Control', {
            'fields': ('assigned_students',)
        }),
        ('Status', {
            'fields': ('is_published',)
        })
    )
    
    def assigned_count(self, obj):
        return obj.assigned_students.count()
    assigned_count.short_description = 'Assigned Students'