from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()

class Province(models.Model):
    """Zambian Provinces"""
    PROVINCES = [
        ('central', 'Central Province'),
        ('copperbelt', 'Copperbelt Province'),
        ('eastern', 'Eastern Province'),
        ('luapula', 'Luapula Province'),
        ('lusaka', 'Lusaka Province'),
        ('muchinga', 'Muchinga Province'),
        ('northern', 'Northern Province'),
        ('northwestern', 'North-Western Province'),
        ('southern', 'Southern Province'),
        ('western', 'Western Province'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVINCES, unique=True)
    capital = models.CharField(max_length=100)
    population = models.PositiveIntegerField(blank=True, null=True)
    area_km2 = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_name_display()

class District(models.Model):
    """Zambian Districts"""
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    population = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['province', 'name']
    
    def __str__(self):
        return f"{self.name}, {self.province.get_name_display()}"

class School(models.Model):
    """Schools in Zambia"""
    SCHOOL_TYPES = [
        ('government', 'Government School'),
        ('private', 'Private School'),
        ('community', 'Community School'),
        ('grant_aided', 'Grant-Aided School'),
    ]
    
    EDUCATION_LEVELS = [
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('combined', 'Combined School'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='schools')
    address = models.TextField()
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # School Details
    established_year = models.PositiveIntegerField(blank=True, null=True)
    total_students = models.PositiveIntegerField(default=0)
    total_teachers = models.PositiveIntegerField(default=0)
    
    # Infrastructure
    has_electricity = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    has_library = models.BooleanField(default=False)
    has_computer_lab = models.BooleanField(default=False)
    has_science_lab = models.BooleanField(default=False)
    
    # Registration
    moe_registration_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.district}"

class Grade(models.Model):
    """Education Grades in Zambian System"""
    GRADE_LEVELS = [
        ('grade_1', 'Grade 1'),
        ('grade_2', 'Grade 2'),
        ('grade_3', 'Grade 3'),
        ('grade_4', 'Grade 4'),
        ('grade_5', 'Grade 5'),
        ('grade_6', 'Grade 6'),
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('grade_11', 'Grade 11'),
        ('grade_12', 'Grade 12'),
    ]
    
    EDUCATION_PHASES = [
        ('primary', 'Primary Education'),
        ('junior_secondary', 'Junior Secondary'),
        ('senior_secondary', 'Senior Secondary'),
    ]
    
    level = models.CharField(max_length=20, choices=GRADE_LEVELS, unique=True)
    phase = models.CharField(max_length=20, choices=EDUCATION_PHASES)
    description = models.TextField(blank=True)
    
    # Age range
    typical_age_min = models.PositiveIntegerField()
    typical_age_max = models.PositiveIntegerField()
    
    # ECZ Examination
    has_ecz_exam = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_level_display()

class Subject(models.Model):
    """Subjects in Zambian Curriculum"""
    SUBJECT_CATEGORIES = [
        ('core', 'Core Subject'),
        ('optional', 'Optional Subject'),
        ('practical', 'Practical Subject'),
        ('language', 'Language Subject'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=20, choices=SUBJECT_CATEGORIES)
    description = models.TextField(blank=True)
    
    # Applicable grades
    grades = models.ManyToManyField(Grade, related_name='subjects')
    
    # ECZ Information
    is_ecz_subject = models.BooleanField(default=False)
    ecz_subject_code = models.CharField(max_length=10, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Curriculum(models.Model):
    """Zambian National Curriculum"""
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='curricula')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='curricula')
    
    # Curriculum Content
    learning_outcomes = models.JSONField(default=list)
    topics = models.JSONField(default=list)
    assessment_criteria = models.JSONField(default=list)
    
    # Resources
    textbooks = models.JSONField(default=list)
    digital_resources = models.JSONField(default=list)
    
    # Timing
    term_1_topics = models.JSONField(default=list)
    term_2_topics = models.JSONField(default=list)
    term_3_topics = models.JSONField(default=list)
    
    # Approval
    approved_by_moe = models.BooleanField(default=False)
    approval_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['subject', 'grade']
    
    def __str__(self):
        return f"{self.subject.name} - {self.grade.get_level_display()}"

class Teacher(models.Model):
    """Teacher Information"""
    QUALIFICATION_LEVELS = [
        ('certificate', 'Teaching Certificate'),
        ('diploma', 'Teaching Diploma'),
        ('degree', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('phd', 'PhD'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    
    # Professional Information
    teacher_registration_number = models.CharField(max_length=50, unique=True)
    qualification_level = models.CharField(max_length=20, choices=QUALIFICATION_LEVELS)
    specialization_subjects = models.ManyToManyField(Subject, related_name='specialized_teachers')
    
    # Employment
    current_school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    years_of_experience = models.PositiveIntegerField(default=0)
    
    # Professional Development
    continuous_professional_development_hours = models.PositiveIntegerField(default=0)
    last_training_date = models.DateField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    tsc_registration_status = models.CharField(max_length=20, default='pending')  # Teaching Service Commission
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.teacher_registration_number}"

class Student(models.Model):
    """Student Information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # Academic Information
    current_grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name='students')
    current_school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    
    # Guardian Information
    guardian_name = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=20)
    guardian_email = models.EmailField(blank=True)
    
    # Academic Records
    subjects_enrolled = models.ManyToManyField(Subject, related_name='enrolled_students')
    
    # Status
    is_active = models.BooleanField(default=True)
    enrollment_date = models.DateField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.current_grade}"

class AcademicYear(models.Model):
    """Academic Year Management"""
    year = models.PositiveIntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Terms
    term_1_start = models.DateField()
    term_1_end = models.DateField()
    term_2_start = models.DateField()
    term_2_end = models.DateField()
    term_3_start = models.DateField()
    term_3_end = models.DateField()
    
    is_current = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Academic Year {self.year}"
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one academic year is current
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)