from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    MobileMoneyProvider, 
    MobileMoneyTransaction, 
    PaymentVerification, 
    SMSNotification,
    PaymentSettings
)

@admin.register(MobileMoneyProvider)
class MobileMoneyProviderAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'ussd_code', 'is_active', 'created_at']
    list_filter = ['is_active', 'name']
    search_fields = ['display_name', 'name']
    readonly_fields = ['created_at', 'updated_at']

class PaymentVerificationInline(admin.TabularInline):
    model = PaymentVerification
    extra = 0
    readonly_fields = ['verified_at']

class SMSNotificationInline(admin.TabularInline):
    model = SMSNotification
    extra = 0
    readonly_fields = ['sent_at']

@admin.register(MobileMoneyTransaction)
class MobileMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'reference_code', 'user_email', 'course_title', 'provider_name', 
        'amount', 'status', 'created_at', 'expires_at', 'action_buttons'
    ]
    list_filter = ['status', 'provider__name', 'currency', 'created_at']
    search_fields = ['reference_code', 'phone_number', 'user__email', 'course__title']
    readonly_fields = ['id', 'reference_code', 'created_at', 'updated_at', 'is_expired']
    inlines = [PaymentVerificationInline, SMSNotificationInline]
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('id', 'reference_code', 'user', 'course', 'provider')
        }),
        ('Payment Information', {
            'fields': ('phone_number', 'amount', 'currency', 'status')
        }),
        ('External References', {
            'fields': ('transaction_id', 'external_reference', 'failure_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'expires_at', 'confirmed_at', 'is_expired')
        }),
    )
    
    actions = ['confirm_payments', 'cancel_payments', 'send_reminders']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def course_title(self, obj):
        return obj.course.title[:50]
    course_title.short_description = 'Course'
    
    def provider_name(self, obj):
        return obj.provider.display_name
    provider_name.short_description = 'Provider'
    
    def action_buttons(self, obj):
        if obj.status == 'pending':
            confirm_url = reverse('admin:confirm_payment', args=[obj.id])
            cancel_url = reverse('admin:cancel_payment', args=[obj.id])
            return format_html(
                '<a class="button" href="{}">Confirm</a> '
                '<a class="button" href="{}">Cancel</a>',
                confirm_url, cancel_url
            )
        return '-'
    action_buttons.short_description = 'Actions'
    
    def confirm_payments(self, request, queryset):
        updated = 0
        for transaction in queryset.filter(status='pending'):
            transaction.status = 'confirmed'
            transaction.confirmed_at = timezone.now()
            transaction.save()
            
            # Create verification record
            PaymentVerification.objects.create(
                transaction=transaction,
                method='admin',
                verified_by=request.user,
                is_successful=True,
                notes=f"Confirmed by admin: {request.user.email}"
            )
            updated += 1
        
        self.message_user(request, f'{updated} payments confirmed successfully.')
    confirm_payments.short_description = "Confirm selected payments"
    
    def cancel_payments(self, request, queryset):
        updated = queryset.filter(status__in=['initiated', 'pending']).update(status='cancelled')
        self.message_user(request, f'{updated} payments cancelled.')
    cancel_payments.short_description = "Cancel selected payments"
    
    def send_reminders(self, request, queryset):
        from .services import SMSService
        sms_service = SMSService()
        sent = 0
        
        for transaction in queryset.filter(status='pending'):
            if sms_service.send_payment_reminder(transaction):
                sent += 1
        
        self.message_user(request, f'{sent} reminder SMS sent.')
    send_reminders.short_description = "Send payment reminders"

@admin.register(PaymentVerification)
class PaymentVerificationAdmin(admin.ModelAdmin):
    list_display = ['transaction_reference', 'method', 'verified_by', 'is_successful', 'verified_at']
    list_filter = ['method', 'is_successful', 'verified_at']
    search_fields = ['transaction__reference_code', 'notes']
    readonly_fields = ['verified_at']
    
    def transaction_reference(self, obj):
        return obj.transaction.reference_code
    transaction_reference.short_description = 'Reference Code'

@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'notification_type', 'delivered', 'sent_at']
    list_filter = ['notification_type', 'delivered', 'sent_at']
    search_fields = ['phone_number', 'message']
    readonly_fields = ['sent_at']

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not PaymentSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
