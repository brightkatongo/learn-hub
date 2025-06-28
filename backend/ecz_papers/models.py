from django.db import models
from django.contrib.auth import get_user_model
from zambian_education.models import Subject, Grade
import uuid

User = get_user_model()

class ECZExaminationSession(models.Model):
    """ECZ Examination Sessions"""
    EXAMINATION_TYPES = [
        ('grade_7', 'Grade 7 Examination'),
        ('grade_9', 'Grade 9 Examination'),
        ('grade_12', 'Grade 12 Examination'),
    ]
    
    SESSIONS = [
        ('march', 'March Session'),
        ('october', 'October Session'),
        ('special', 'Special Session'),
    ]
    
    year = models.PositiveIntegerField()
    session = models.CharField(max_length=20, choices=SESSIONS)
    examination_type = models.CharField(max_length=20, choices=EXAMINATION_TYPES)
    
    # Dates
    registration_start = models.DateField()
    registration_end = models.DateField()
    examination_start = models.DateField()
    examination_end = models.DateField()
    results_release_date = models.DateField(blank=True, null=True)
    
    # Fees
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    late_registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['year', 'session', 'examination_type']
    
    def __str__(self):
        return f"{self.get_examination_type_display()} - {self.get_session_display()} {self.year}"

class ECZPaper(models.Model):
    """ECZ Examination Papers"""
    PAPER_TYPES = [
        ('paper_1', 'Paper 1'),
        ('paper_2', 'Paper 2'),
        ('paper_3', 'Paper 3'),
        ('practical', 'Practical Paper'),
        ('oral', 'Oral Paper'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ECZExaminationSession, on_delete=models.CASCADE, related_name='papers')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ecz_papers')
    paper_type = models.CharField(max_length=20, choices=PAPER_TYPES)
    
    # Paper Details
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    
    # Files
    question_paper = models.FileField(upload_to='ecz_papers/questions/', blank=True, null=True)
    marking_scheme = models.FileField(upload_to='ecz_papers/marking_schemes/', blank=True, null=True)
    
    # Content
    instructions = models.TextField()
    sections = models.JSONField(default=list)  # Paper sections with questions
    
    # Statistics
    total_candidates = models.PositiveIntegerField(default=0)
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Access Control
    is_public = models.BooleanField(default=False)
    release_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session', 'subject', 'paper_type']
    
    def __str__(self):
        return f"{self.subject.name} {self.get_paper_type_display()} - {self.session}"

class PastPaper(models.Model):
    """Historical Past Papers Collection"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='past_papers')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='past_papers')
    
    year = models.PositiveIntegerField()
    session = models.CharField(max_length=20, choices=ECZExaminationSession.SESSIONS)
    paper_type = models.CharField(max_length=20, choices=ECZPaper.PAPER_TYPES)
    
    # Files
    question_paper_url = models.URLField(blank=True)
    marking_scheme_url = models.URLField(blank=True)
    question_paper_file = models.FileField(upload_to='past_papers/questions/', blank=True, null=True)
    marking_scheme_file = models.FileField(upload_to='past_papers/marking_schemes/', blank=True, null=True)
    
    # Metadata
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    
    # Usage Statistics
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # Quality Control
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_papers')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['subject', 'grade', 'year', 'session', 'paper_type']
    
    def __str__(self):
        return f"{self.subject.name} {self.get_paper_type_display()} - {self.year} {self.get_session_display()}"

class ECZSyllabus(models.Model):
    """ECZ Syllabus Documents"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='syllabi')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='syllabi')
    
    title = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    effective_year = models.PositiveIntegerField()
    
    # Content
    aims_and_objectives = models.TextField()
    assessment_objectives = models.TextField()
    content_outline = models.JSONField(default=list)
    assessment_scheme = models.JSONField(default=dict)
    
    # Files
    syllabus_document = models.FileField(upload_to='syllabi/', blank=True, null=True)
    syllabus_url = models.URLField(blank=True)
    
    # Status
    is_current = models.BooleanField(default=True)
    approved_by_ecz = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['subject', 'grade', 'version']
        verbose_name_plural = 'ECZ Syllabi'
    
    def __str__(self):
        return f"{self.subject.name} Syllabus - {self.grade.get_level_display()} (v{self.version})"

class StudentPaperAttempt(models.Model):
    """Track student attempts on past papers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper_attempts')
    paper = models.ForeignKey(PastPaper, on_delete=models.CASCADE, related_name='attempts')
    
    # Attempt Details
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Scoring
    total_score = models.PositiveIntegerField(default=0)
    percentage_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Answers
    answers = models.JSONField(default=dict)  # Question ID -> Answer mapping
    
    # Analysis
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.paper} ({self.percentage_score}%)"

class ECZResultsAnalysis(models.Model):
    """Analysis of ECZ Results by various demographics"""
    session = models.ForeignKey(ECZExaminationSession, on_delete=models.CASCADE, related_name='results_analysis')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results_analysis')
    
    # Overall Statistics
    total_candidates = models.PositiveIntegerField()
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2)
    distinction_rate = models.DecimalField(max_digits=5, decimal_places=2)
    credit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Grade Distribution
    grade_distribution = models.JSONField(default=dict)  # Grade -> Count
    
    # Performance by Demographics
    performance_by_gender = models.JSONField(default=dict)
    performance_by_province = models.JSONField(default=dict)
    performance_by_school_type = models.JSONField(default=dict)
    
    # Trends
    comparison_with_previous_year = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'subject']
        verbose_name_plural = 'ECZ Results Analyses'
    
    def __str__(self):
        return f"{self.subject.name} Results Analysis - {self.session}"