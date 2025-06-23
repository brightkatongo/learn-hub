from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = models.CharField(
        max_length=17,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        blank=True
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # Additional fields for better user management
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    login_count = models.PositiveIntegerField(default=0)
    is_active_subscription = models.BooleanField(default=True)
    subscription_expires = models.DateTimeField(blank=True, null=True)
    
    # Location and preferences
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language_preference = models.CharField(max_length=10, default='en')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active']),
        ]
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Return the full name of the user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def update_login_info(self, ip_address=None):
        """Update login information"""
        self.last_login = timezone.now()
        self.login_count += 1
        if ip_address:
            self.last_login_ip = ip_address
        self.save(update_fields=['last_login', 'login_count', 'last_login_ip'])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    learning_goals = models.TextField(blank=True)
    interests = models.JSONField(default=list, blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    
    # Learning preferences
    preferred_learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Visual'),
            ('auditory', 'Auditory'),
            ('kinesthetic', 'Kinesthetic'),
            ('reading', 'Reading/Writing'),
        ],
        blank=True
    )
    
    # Privacy settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('friends', 'Friends Only'),
        ],
        default='public'
    )
    
    # Achievements and progress
    total_courses_completed = models.PositiveIntegerField(default=0)
    total_certificates_earned = models.PositiveIntegerField(default=0)
    total_learning_hours = models.PositiveIntegerField(default=0)
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} Profile"

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    expertise = models.JSONField(default=list, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True)
    certifications = models.JSONField(default=list, blank=True)
    
    # Professional information
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    # Teaching preferences
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_for_consultation = models.BooleanField(default=False)
    consultation_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Approval and verification
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_instructors'
    )
    
    # Statistics
    total_students = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Payout information
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    mobile_money_number = models.CharField(max_length=20, blank=True)
    preferred_payout_method = models.CharField(
        max_length=20,
        choices=[
            ('bank', 'Bank Transfer'),
            ('mobile_money', 'Mobile Money'),
            ('paypal', 'PayPal'),
        ],
        default='mobile_money'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} Instructor Profile"
    
    def update_statistics(self):
        """Update instructor statistics"""
        from courses.models import Course, Enrollment
        
        courses = Course.objects.filter(instructor=self.user)
        self.total_courses = courses.count()
        
        enrollments = Enrollment.objects.filter(course__instructor=self.user)
        self.total_students = enrollments.values('user').distinct().count()
        
        # Calculate revenue
        completed_enrollments = enrollments.filter(payment_status='completed')
        self.total_revenue = sum(e.amount_paid for e in completed_enrollments)
        
        # Calculate average rating
        from courses.models import Review
        reviews = Review.objects.filter(course__instructor=self.user)
        if reviews.exists():
            self.average_rating = reviews.aggregate(
                avg_rating=models.Avg('rating')
            )['avg_rating'] or 0
            self.total_reviews = reviews.count()
        
        self.save()

class UserSession(models.Model):
    """Track user sessions for analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    # Session data
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Location data (optional)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'started_at']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.started_at}"
    
    def end_session(self):
        """End the session and calculate duration"""
        if not self.ended_at:
            self.ended_at = timezone.now()
            self.duration_seconds = (self.ended_at - self.started_at).total_seconds()
            self.save()

class UserPreferences(models.Model):
    """User preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    
    # Course notifications
    course_updates = models.BooleanField(default=True)
    new_lectures = models.BooleanField(default=True)
    assignment_reminders = models.BooleanField(default=True)
    certificate_notifications = models.BooleanField(default=True)
    
    # Marketing preferences
    promotional_emails = models.BooleanField(default=False)
    course_recommendations = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=False)
    
    # Privacy preferences
    show_profile_publicly = models.BooleanField(default=True)
    show_learning_progress = models.BooleanField(default=True)
    allow_instructor_contact = models.BooleanField(default=True)
    
    # Learning preferences
    auto_play_videos = models.BooleanField(default=True)
    video_quality = models.CharField(
        max_length=10,
        choices=[
            ('auto', 'Auto'),
            ('720p', '720p'),
            ('1080p', '1080p'),
        ],
        default='auto'
    )
    playback_speed = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} Preferences"