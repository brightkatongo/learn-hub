from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
import uuid
from django.utils import timezone
import secrets
import string

User = get_user_model()

class MobileMoneyProvider(models.Model):
    PROVIDER_CHOICES = [
        ('airtel', 'Airtel Money'),
        ('zamtel', 'Zamtel Money'),
        ('mtn', 'MTN Money'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    ussd_code = models.CharField(max_length=10)
    merchant_code = models.CharField(max_length=50, blank=True)
    business_number = models.CharField(max_length=50, blank=True)
    payee_code = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    phone_prefixes = models.JSONField(default=list)  # ['097', '096', '095']
    instructions = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.display_name

class MobileMoneyTransaction(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Payment Initiated'),
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Payment Confirmed'),
        ('failed', 'Payment Failed'),
        ('expired', 'Payment Expired'),
        ('cancelled', 'Payment Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mobile_transactions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='mobile_payments')
    provider = models.ForeignKey(MobileMoneyProvider, on_delete=models.CASCADE)
    
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='ZMW')
    
    reference_code = models.CharField(max_length=10, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    external_reference = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    failure_reason = models.TextField(blank=True)
    
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference_code']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self.generate_reference_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=30)
        super().save(*args, **kwargs)
    
    def generate_reference_code(self):
        """Generate a unique 8-digit reference code"""
        while True:
            code = ''.join(secrets.choice(string.digits) for _ in range(8))
            if not MobileMoneyTransaction.objects.filter(reference_code=code).exists():
                return code
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at and self.status in ['initiated', 'pending']
    
    def __str__(self):
        return f"{self.provider.display_name} - {self.reference_code} - {self.amount} {self.currency}"

class PaymentVerification(models.Model):
    VERIFICATION_METHODS = [
        ('sms', 'SMS Confirmation'),
        ('manual', 'Manual Verification'),
        ('webhook', 'Webhook Callback'),
        ('admin', 'Admin Confirmation'),
    ]
    
    transaction = models.ForeignKey(MobileMoneyTransaction, on_delete=models.CASCADE, related_name='verifications')
    method = models.CharField(max_length=20, choices=VERIFICATION_METHODS)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    verification_data = models.JSONField(default=dict)  # Store SMS content, webhook data, etc.
    notes = models.TextField(blank=True)
    
    is_successful = models.BooleanField(default=False)
    verified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Verification for {self.transaction.reference_code} - {self.method}"

class SMSNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('payment_instructions', 'Payment Instructions'),
        ('payment_reminder', 'Payment Reminder'),
        ('payment_confirmed', 'Payment Confirmed'),
        ('payment_failed', 'Payment Failed'),
    ]
    
    transaction = models.ForeignKey(MobileMoneyTransaction, on_delete=models.CASCADE, related_name='sms_notifications')
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"SMS to {self.phone_number} - {self.notification_type}"

class PaymentSettings(models.Model):
    """Global settings for mobile money payments"""
    payment_timeout_minutes = models.PositiveIntegerField(default=30)
    max_payment_attempts = models.PositiveIntegerField(default=3)
    sms_provider = models.CharField(max_length=50, default='africas_talking')
    auto_verification_enabled = models.BooleanField(default=False)
    
    # SMS Templates
    payment_instructions_template = models.TextField(
        default="Complete your payment of {amount} {currency} for {course_title}. "
                "Dial {ussd_code} and use reference: {reference_code}"
    )
    payment_confirmed_template = models.TextField(
        default="Payment confirmed! You now have access to {course_title}. "
                "Reference: {reference_code}"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Payment Settings"
    
    def __str__(self):
        return "Payment Settings"
