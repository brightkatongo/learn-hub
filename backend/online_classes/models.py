from django.db import models
from django.contrib.auth import get_user_model
from zambian_education.models import Subject, Grade, Teacher, Student
from courses.models import Course
import uuid

User = get_user_model()

class LiveClassroom(models.Model):
    """Virtual Classroom for Live Classes"""
    CLASS_TYPES = [
        ('regular', 'Regular Class'),
        ('revision', 'Revision Class'),
        ('exam_prep', 'Exam Preparation'),
        ('remedial', 'Remedial Class'),
        ('enrichment', 'Enrichment Class'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Details
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='live_classes')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='live_classes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='live_classes')
    
    # Class Details
    class_type = models.CharField(max_length=20, choices=CLASS_TYPES, default='regular')
    topic = models.CharField(max_length=300)
    learning_objectives = models.JSONField(default=list)
    
    # Scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    
    # Capacity
    max_students = models.PositiveIntegerField(default=50)
    enrolled_students = models.ManyToManyField(Student, through='ClassEnrollment', related_name='enrolled_classes')
    
    # Technology
    meeting_platform = models.CharField(max_length=50, choices=[
        ('zoom', 'Zoom'),
        ('teams', 'Microsoft Teams'),
        ('meet', 'Google Meet'),
        ('webex', 'Cisco Webex'),
        ('custom', 'Custom Platform'),
    ], default='zoom')
    meeting_id = models.CharField(max_length=100, blank=True)
    meeting_password = models.CharField(max_length=50, blank=True)
    meeting_url = models.URLField(blank=True)
    
    # Content
    presentation_slides = models.FileField(upload_to='live_classes/slides/', blank=True, null=True)
    additional_resources = models.JSONField(default=list)
    
    # Recording
    is_recorded = models.BooleanField(default=True)
    recording_url = models.URLField(blank=True)
    recording_file = models.FileField(upload_to='live_classes/recordings/', blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Analytics
    peak_attendance = models.PositiveIntegerField(default=0)
    average_attendance_duration = models.PositiveIntegerField(default=0)  # in minutes
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.grade.get_level_display()})"

class ClassEnrollment(models.Model):
    """Student Enrollment in Live Classes"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(LiveClassroom, on_delete=models.CASCADE)
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    attendance_duration = models.PositiveIntegerField(default=0)  # in minutes
    
    # Participation
    questions_asked = models.PositiveIntegerField(default=0)
    chat_messages = models.PositiveIntegerField(default=0)
    
    # Feedback
    rating = models.PositiveIntegerField(blank=True, null=True, choices=[
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')
    ])
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student', 'classroom']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.classroom.title}"

class EducationalVideo(models.Model):
    """Educational Video Content"""
    VIDEO_TYPES = [
        ('lesson', 'Lesson Video'),
        ('tutorial', 'Tutorial'),
        ('lecture', 'Lecture'),
        ('demonstration', 'Demonstration'),
        ('experiment', 'Science Experiment'),
        ('documentary', 'Educational Documentary'),
    ]
    
    QUALITY_LEVELS = [
        ('240p', '240p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p HD'),
        ('1080p', '1080p Full HD'),
        ('4k', '4K Ultra HD'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Classification
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='videos')
    topic = models.CharField(max_length=200)
    
    # Video Details
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES, default='lesson')
    duration_seconds = models.PositiveIntegerField()
    quality = models.CharField(max_length=10, choices=QUALITY_LEVELS, default='720p')
    
    # Files
    video_file = models.FileField(upload_to='educational_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True)  # For external hosting
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    subtitles_file = models.FileField(upload_to='video_subtitles/', blank=True, null=True)
    
    # Metadata
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    has_subtitles = models.BooleanField(default=False)
    
    # Educational Content
    learning_objectives = models.JSONField(default=list)
    curriculum_alignment = models.JSONField(default=list)
    prerequisites = models.JSONField(default=list)
    
    # Creator and Quality
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_videos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_videos')
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_watch_time_hours = models.PositiveIntegerField(default=0)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    
    # SEO and Discovery
    tags = models.JSONField(default=list)
    keywords = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subject', 'grade']),
            models.Index(fields=['is_published', 'is_featured']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.grade.get_level_display()})"
    
    @property
    def duration_formatted(self):
        """Return duration in HH:MM:SS format"""
        hours = self.duration_seconds // 3600
        minutes = (self.duration_seconds % 3600) // 60
        seconds = self.duration_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

class VideoWatchHistory(models.Model):
    """Track video watching history and progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_history')
    video = models.ForeignKey(EducationalVideo, on_delete=models.CASCADE, related_name='watch_history')
    
    # Progress tracking
    watch_time_seconds = models.PositiveIntegerField(default=0)
    last_position_seconds = models.PositiveIntegerField(default=0)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    
    # Session tracking
    first_watched = models.DateTimeField(auto_now_add=True)
    last_watched = models.DateTimeField(auto_now=True)
    total_sessions = models.PositiveIntegerField(default=1)
    
    # Engagement
    liked = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(blank=True, null=True, choices=[
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')
    ])
    
    class Meta:
        unique_together = ['user', 'video']
        ordering = ['-last_watched']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.video.title} ({self.completion_percentage}%)"

class ClassSchedule(models.Model):
    """Weekly Class Schedule"""
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Recurrence
    is_recurring = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Classroom
    virtual_classroom = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['subject', 'grade', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.subject.name} - {self.grade.get_level_display()} ({self.get_day_of_week_display()} {self.start_time})"

class StudyGroup(models.Model):
    """Student Study Groups"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Focus
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='study_groups')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='study_groups')
    
    # Members
    creator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField(Student, related_name='study_groups')
    moderator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_groups')
    
    # Settings
    max_members = models.PositiveIntegerField(default=20)
    is_public = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Meeting Details
    regular_meeting_day = models.CharField(max_length=10, choices=ClassSchedule.DAYS_OF_WEEK, blank=True)
    regular_meeting_time = models.TimeField(blank=True, null=True)
    meeting_platform = models.CharField(max_length=50, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class DigitalResource(models.Model):
    """Digital Learning Resources"""
    RESOURCE_TYPES = [
        ('video', 'Video Lesson'),
        ('audio', 'Audio Lesson'),
        ('document', 'Document'),
        ('presentation', 'Presentation'),
        ('interactive', 'Interactive Content'),
        ('simulation', 'Simulation'),
        ('quiz', 'Quiz'),
        ('worksheet', 'Worksheet'),
    ]
    
    ACCESS_LEVELS = [
        ('free', 'Free Access'),
        ('premium', 'Premium Access'),
        ('school_only', 'School Access Only'),
        ('teacher_only', 'Teacher Access Only'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Classification
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='digital_resources')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='digital_resources')
    topic = models.CharField(max_length=200)
    
    # Resource Details
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='free')
    
    # Files and URLs
    file = models.FileField(upload_to='digital_resources/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='digital_resources/thumbnails/', blank=True, null=True)
    
    # Metadata
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    
    # Educational Alignment
    curriculum_alignment = models.JSONField(default=list)  # Curriculum topics covered
    learning_objectives = models.JSONField(default=list)
    
    # Quality and Usage
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_resources')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_resources')
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.grade.get_level_display()})"

class VirtualLab(models.Model):
    """Virtual Laboratory for Science Subjects"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Details
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='virtual_labs')
    applicable_grades = models.ManyToManyField(Grade, related_name='virtual_labs')
    
    # Lab Details
    lab_type = models.CharField(max_length=50, choices=[
        ('physics', 'Physics Lab'),
        ('chemistry', 'Chemistry Lab'),
        ('biology', 'Biology Lab'),
        ('computer', 'Computer Lab'),
        ('mathematics', 'Mathematics Lab'),
    ])
    
    # Technology
    simulation_url = models.URLField()
    requires_plugin = models.BooleanField(default=False)
    plugin_requirements = models.JSONField(default=list)
    
    # Educational Content
    experiments = models.JSONField(default=list)
    learning_outcomes = models.JSONField(default=list)
    safety_guidelines = models.TextField()
    
    # Access
    is_free = models.BooleanField(default=True)
    requires_supervision = models.BooleanField(default=False)
    
    # Usage Statistics
    total_sessions = models.PositiveIntegerField(default=0)
    average_session_duration = models.PositiveIntegerField(default=0)  # in minutes
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class OnlineAssessment(models.Model):
    """Online Assessments and Quizzes"""
    ASSESSMENT_TYPES = [
        ('quiz', 'Quiz'),
        ('test', 'Test'),
        ('assignment', 'Assignment'),
        ('mock_exam', 'Mock Examination'),
        ('diagnostic', 'Diagnostic Assessment'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Details
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='online_assessments')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='online_assessments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='created_assessments')
    
    # Assessment Configuration
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    total_marks = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    
    # Questions
    questions = models.JSONField(default=list)  # Question data structure
    
    # Timing
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    
    # Settings
    attempts_allowed = models.PositiveIntegerField(default=1)
    show_results_immediately = models.BooleanField(default=False)
    randomize_questions = models.BooleanField(default=False)
    
    # Access Control
    assigned_students = models.ManyToManyField(Student, related_name='assigned_assessments')
    
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.grade.get_level_display()})"