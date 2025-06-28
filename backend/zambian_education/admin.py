from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    Province, District, School, Grade, Subject, Curriculum, 
    Teacher, Student, AcademicYear
)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('get_name_display', 'capital', 'population', 'area_km2', 'district_count')
    list_filter = ('name',)
    search_fields = ('name', 'capital')
    readonly_fields = ('created_at', 'updated_at')
    
    def district_count(self, obj):
        return obj.districts.count()
    district_count.short_description = 'Districts'

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'population', 'school_count')
    list_filter = ('province',)
    search_fields = ('name', 'province__name')
    readonly_fields = ('created_at', 'updated_at')
    
    def school_count(self, obj):
        return obj.schools.count()
    school_count.short_description = 'Schools'

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'school_type', 'education_level', 'district', 
        'total_students', 'total_teachers', 'infrastructure_status'
    )
    list_filter = (
        'school_type', 'education_level', 'district__province', 
        'has_electricity', 'has_internet', 'is_active'
    )
    search_fields = ('name', 'moe_registration_number', 'district__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'school_type', 'education_level', 'district', 'address')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('School Details', {
            'fields': ('established_year', 'total_students', 'total_teachers', 'moe_registration_number')
        }),
        ('Infrastructure', {
            'fields': (
                'has_electricity', 'has_internet', 'has_library', 
                'has_computer_lab', 'has_science_lab'
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def infrastructure_status(self, obj):
        status = []
        if obj.has_electricity:
            status.append('⚡')
        if obj.has_internet:
            status.append('🌐')
        if obj.has_library:
            status.append('📚')
        if obj.has_computer_lab:
            status.append('💻')
        if obj.has_science_lab:
            status.append('🔬')
        return ''.join(status) if status else '❌'
    infrastructure_status.short_description = 'Infrastructure'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('get_level_display', 'phase', 'typical_age_range', 'has_ecz_exam', 'subject_count')
    list_filter = ('phase', 'has_ecz_exam')
    readonly_fields = ('created_at',)
    
    def typical_age_range(self, obj):
        return f"{obj.typical_age_min}-{obj.typical_age_max} years"
    typical_age_range.short_description = 'Age Range'
    
    def subject_count(self, obj):
        return obj.subjects.count()
    subject_count.short_description = 'Subjects'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_ecz_subject', 'ecz_subject_code', 'grade_levels')
    list_filter = ('category', 'is_ecz_subject')
    search_fields = ('name', 'code', 'ecz_subject_code')
    filter_horizontal = ('grades',)
    readonly_fields = ('created_at', 'updated_at')
    
    def grade_levels(self, obj):
        grades = obj.grades.all()[:5]  # Show first 5 grades
        grade_list = [grade.get_level_display() for grade in grades]
        if obj.grades.count() > 5:
            grade_list.append('...')
        return ', '.join(grade_list)
    grade_levels.short_description = 'Grade Levels'

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'approved_by_moe', 'approval_date')
    list_filter = ('approved_by_moe', 'subject__category', 'grade__phase')
    search_fields = ('title', 'subject__name', 'grade__level')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subject', 'grade')
        }),
        ('Content', {
            'fields': ('learning_outcomes', 'topics', 'assessment_criteria')
        }),
        ('Resources', {
            'fields': ('textbooks', 'digital_resources')
        }),
        ('Term Planning', {
            'fields': ('term_1_topics', 'term_2_topics', 'term_3_topics')
        }),
        ('Approval', {
            'fields': ('approved_by_moe', 'approval_date')
        })
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'teacher_registration_number', 'qualification_level', 
        'current_school', 'years_of_experience', 'specialization_subjects_list', 'is_active'
    )
    list_filter = (
        'qualification_level', 'is_active', 'current_school__district__province',
        'tsc_registration_status'
    )
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email', 
        'teacher_registration_number'
    )
    filter_horizontal = ('specialization_subjects',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': (
                'teacher_registration_number', 'qualification_level', 
                'specialization_subjects'
            )
        }),
        ('Employment', {
            'fields': ('current_school', 'years_of_experience')
        }),
        ('Professional Development', {
            'fields': (
                'continuous_professional_development_hours', 'last_training_date'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'tsc_registration_status')
        })
    )
    
    def specialization_subjects_list(self, obj):
        subjects = obj.specialization_subjects.all()[:3]
        subject_list = [subject.name for subject in subjects]
        if obj.specialization_subjects.count() > 3:
            subject_list.append('...')
        return ', '.join(subject_list)
    specialization_subjects_list.short_description = 'Specializations'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'current_grade', 'current_school', 'gender', 
        'guardian_name', 'guardian_phone', 'is_active'
    )
    list_filter = (
        'current_grade', 'gender', 'is_active', 
        'current_school__district__province'
    )
    search_fields = (
        'user__first_name', 'user__last_name', 'user__email',
        'guardian_name', 'guardian_phone'
    )
    filter_horizontal = ('subjects_enrolled',)
    readonly_fields = ('created_at', 'updated_at', 'enrollment_date')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('current_grade', 'current_school', 'subjects_enrolled')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email')
        }),
        ('Status', {
            'fields': ('is_active', 'enrollment_date')
        })
    )

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_current', 'term_info')
    list_filter = ('is_current',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Academic Year', {
            'fields': ('year', 'start_date', 'end_date', 'is_current')
        }),
        ('Term 1', {
            'fields': ('term_1_start', 'term_1_end')
        }),
        ('Term 2', {
            'fields': ('term_2_start', 'term_2_end')
        }),
        ('Term 3', {
            'fields': ('term_3_start', 'term_3_end')
        })
    )
    
    def term_info(self, obj):
        return format_html(
            "T1: {} - {}<br>T2: {} - {}<br>T3: {} - {}",
            obj.term_1_start, obj.term_1_end,
            obj.term_2_start, obj.term_2_end,
            obj.term_3_start, obj.term_3_end
        )
    term_info.short_description = 'Term Dates'