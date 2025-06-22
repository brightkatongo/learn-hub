from django.contrib import admin
from .models import Payment, Coupon, CouponUsage, InstructorPayout

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'amount', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'course__title', 'transaction_id')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'used_count', 'usage_limit', 'is_active', 'valid_until')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'description')
    filter_horizontal = ('applicable_courses',)

@admin.register(InstructorPayout)
class InstructorPayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'instructor', 'amount', 'payout_status', 'period_start', 'period_end', 'created_at')
    list_filter = ('payout_status', 'created_at')
    search_fields = ('instructor__email',)
    readonly_fields = ('id', 'created_at')
