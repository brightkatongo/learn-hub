from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import (
    ECZExaminationSession, ECZPaper, PastPaper, ECZSyllabus,
    StudentPaperAttempt, ECZResultsAnalysis
)

@admin.register(ECZExaminationSession)
class ECZExaminationSessionAdmin(admin.ModelAdmin):
    list_display = (
        'year', 'session', 'examination_type', 'registration_period', 
        'examination_period', 'registration_fee', 'paper_count', 'is_active'
    )
    list_filter = ('examination_type', 'session', 'is_active', 'year')
    search_fields = ('year',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Session Information', {
            'fields': ('year', 'session', 'examination_type', 'is_active')
        }),
        ('Registration Period', {
            'fields': ('registration_start', 'registration_end')
        }),
        ('Examination Period', {
            'fields': ('examination_start', 'examination_end', 'results_release_date')
        }),
        ('Fees', {
            'fields': ('registration_fee', 'late_registration_fee')
        })
    )
    
    def registration_period(self, obj):
        return f"{obj.registration_start} to {obj.registration_end}"
    registration_period.short_description = 'Registration Period'
    
    def examination_period(self, obj):
        return f"{obj.examination_start} to {obj.examination_end}"
    examination_period.short_description = 'Examination Period'
    
    def paper_count(self, obj):
        return obj.papers.count()
    paper_count.short_description = 'Papers'

@admin.register(ECZPaper)
class ECZPaperAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'session', 'subject', 'paper_type', 'duration_minutes',
        'total_marks', 'total_candidates', 'pass_rate', 'is_public'
    )
    list_filter = (
        'session__examination_type', 'session__year', 'paper_type', 
        'subject__category', 'is_public'
    )
    search_fields = ('title', 'subject__name', 'session__year')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Paper Information', {
            'fields': ('session', 'subject', 'paper_type', 'title')
        }),
        ('Paper Details', {
            'fields': ('duration_minutes', 'total_marks', 'instructions')
        }),
        ('Content', {
            'fields': ('sections',)
        }),
        ('Files', {
            'fields': ('question_paper', 'marking_scheme')
        }),
        ('Statistics', {
            'fields': ('total_candidates', 'pass_rate')
        }),
        ('Access Control', {
            'fields': ('is_public', 'release_date')
        })
    )

@admin.register(PastPaper)
class PastPaperAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 'grade', 'year', 'session', 'paper_type',
        'difficulty_level', 'download_count', 'view_count', 'is_verified'
    )
    list_filter = (
        'grade__level', 'subject__category', 'year', 'session',
        'paper_type', 'difficulty_level', 'is_verified'
    )
    search_fields = ('subject__name', 'year')
    readonly_fields = ('id', 'created_at', 'updated_at', 'download_count', 'view_count')
    
    fieldsets = (
        ('Paper Information', {
            'fields': ('subject', 'grade', 'year', 'session', 'paper_type')
        }),
        ('Paper Details', {
            'fields': ('duration_minutes', 'total_marks', 'difficulty_level')
        }),
        ('Files', {
            'fields': (
                'question_paper_file', 'marking_scheme_file',
                'question_paper_url', 'marking_scheme_url'
            )
        }),
        ('Quality Control', {
            'fields': ('is_verified', 'verified_by')
        }),
        ('Statistics', {
            'fields': ('download_count', 'view_count')
        })
    )
    
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True, verified_by=request.user)
        self.message_user(request, f'{updated} papers marked as verified.')
    mark_as_verified.short_description = "Mark selected papers as verified"
    
    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False, verified_by=None)
        self.message_user(request, f'{updated} papers marked as unverified.')
    mark_as_unverified.short_description = "Mark selected papers as unverified"

@admin.register(ECZSyllabus)
class ECZSyllabusAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'grade', 'version', 'effective_year',
        'is_current', 'approved_by_ecz'
    )
    list_filter = (
        'subject__category', 'grade__level', 'is_current', 
        'approved_by_ecz', 'effective_year'
    )
    search_fields = ('title', 'subject__name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Syllabus Information', {
            'fields': ('title', 'subject', 'grade', 'version', 'effective_year')
        }),
        ('Content', {
            'fields': ('aims_and_objectives', 'assessment_objectives')
        }),
        ('Curriculum Structure', {
            'fields': ('content_outline', 'assessment_scheme')
        }),
        ('Documents', {
            'fields': ('syllabus_document', 'syllabus_url')
        }),
        ('Status', {
            'fields': ('is_current', 'approved_by_ecz')
        })
    )

@admin.register(StudentPaperAttempt)
class StudentPaperAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'paper', 'started_at', 'completed_at',
        'time_spent_minutes', 'percentage_score', 'is_completed'
    )
    list_filter = (
        'paper__subject', 'paper__grade', 'is_completed',
        'started_at', 'paper__year'
    )
    search_fields = (
        'student__first_name', 'student__last_name', 'student__email',
        'paper__subject__name'
    )
    readonly_fields = ('id', 'started_at')
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('student', 'paper', 'started_at', 'completed_at')
        }),
        ('Performance', {
            'fields': ('time_spent_minutes', 'total_score', 'percentage_score')
        }),
        ('Answers', {
            'fields': ('answers',)
        }),
        ('Analysis', {
            'fields': ('strengths', 'weaknesses', 'recommendations')
        }),
        ('Status', {
            'fields': ('is_completed',)
        })
    )

@admin.register(ECZResultsAnalysis)
class ECZResultsAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'session', 'subject', 'total_candidates', 'pass_rate',
        'distinction_rate', 'credit_rate'
    )
    list_filter = (
        'session__examination_type', 'session__year', 'subject__category'
    )
    search_fields = ('subject__name', 'session__year')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Analysis Information', {
            'fields': ('session', 'subject')
        }),
        ('Overall Statistics', {
            'fields': (
                'total_candidates', 'pass_rate', 'distinction_rate', 'credit_rate'
            )
        }),
        ('Grade Distribution', {
            'fields': ('grade_distribution',)
        }),
        ('Performance Analysis', {
            'fields': (
                'performance_by_gender', 'performance_by_province',
                'performance_by_school_type'
            )
        }),
        ('Trends', {
            'fields': ('comparison_with_previous_year',)
        })
    )