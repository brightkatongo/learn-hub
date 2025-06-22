import re
from typing import Optional, Dict, Any
from django.conf import settings
from django.utils import timezone
from .models import MobileMoneyTransaction, MobileMoneyProvider, SMSNotification, PaymentSettings
from courses.models import Enrollment

class PhoneNumberValidator:
    """Validate and format Zambian phone numbers"""
    
    PROVIDER_PREFIXES = {
        'airtel': ['097', '096', '095'],
        'zamtel': ['095', '094'],
        'mtn': ['096', '097', '098']
    }
    
    @classmethod
    def clean_phone_number(cls, phone: str) -> str:
        """Clean and format phone number"""
        # Remove all non-digits
        phone = re.sub(r'\D', '', phone)
        
        # Handle different formats
        if phone.startswith('260'):
            phone = phone[3:]  # Remove country code
        elif phone.startswith('0'):
            phone = phone[1:]  # Remove leading zero
        
        return phone
    
    @classmethod
    def detect_provider(cls, phone: str) -> Optional[str]:
        """Detect mobile money provider from phone number"""
        clean_phone = cls.clean_phone_number(phone)
        
        if len(clean_phone) != 9:
            return None
        
        prefix = clean_phone[:3]
        
        for provider, prefixes in cls.PROVIDER_PREFIXES.items():
            if prefix in prefixes:
                return provider
        
        return None
    
    @classmethod
    def format_phone_number(cls, phone: str) -> str:
        """Format phone number for display"""
        clean_phone = cls.clean_phone_number(phone)
        if len(clean_phone) == 9:
            return f"+260 {clean_phone[:2]} {clean_phone[2:5]} {clean_phone[5:]}"
        return phone

class USSDInstructionGenerator:
    """Generate USSD instructions for different providers"""
    
    @staticmethod
    def get_instructions(provider_name: str, transaction: MobileMoneyTransaction) -> Dict[str, Any]:
        """Get step-by-step USSD instructions"""
        
        instructions = {
            'airtel': {
                'steps': [
                    f"Dial *778# on your Airtel phone",
                    "Select option 1: Send Money",
                    "Select option 2: Pay Bill",
                    f"Enter Merchant Code: {transaction.provider.merchant_code}",
                    f"Enter Amount: {transaction.amount}",
                    f"Enter Reference: {transaction.reference_code}",
                    "Enter your PIN to confirm",
                    "Wait for confirmation SMS"
                ],
                'ussd_code': '*778#',
                'estimated_time': '2-3 minutes'
            },
            'zamtel': {
                'steps': [
                    f"Dial *776# on your Zamtel phone",
                    "Select option 2: Pay Bill",
                    f"Enter Business Number: {transaction.provider.business_number}",
                    f"Enter Amount: {transaction.amount}",
                    f"Enter Reference: {transaction.reference_code}",
                    "Enter your PIN to confirm",
                    "Wait for confirmation SMS"
                ],
                'ussd_code': '*776#',
                'estimated_time': '2-3 minutes'
            },
            'mtn': {
                'steps': [
                    f"Dial *175# on your MTN phone",
                    "Select option 1: Send Money",
                    "Select option 2: Pay Bill",
                    f"Enter Payee Code: {transaction.provider.payee_code}",
                    f"Enter Amount: {transaction.amount}",
                    f"Enter Reference: {transaction.reference_code}",
                    "Enter your PIN to confirm",
                    "Wait for confirmation SMS"
                ],
                'ussd_code': '*175#',
                'estimated_time': '2-3 minutes'
            }
        }
        
        return instructions.get(provider_name, {})

class SMSService:
    """Handle SMS notifications for payments"""
    
    def __init__(self):
        self.settings = PaymentSettings.objects.first()
        if not self.settings:
            self.settings = PaymentSettings.objects.create()
    
    def send_payment_instructions(self, transaction: MobileMoneyTransaction) -> bool:
        """Send payment instructions via SMS"""
        message = self.settings.payment_instructions_template.format(
            amount=transaction.amount,
            currency=transaction.currency,
            course_title=transaction.course.title,
            ussd_code=transaction.provider.ussd_code,
            reference_code=transaction.reference_code
        )
        
        return self._send_sms(
            transaction=transaction,
            phone_number=transaction.phone_number,
            message=message,
            notification_type='payment_instructions'
        )
    
    def send_payment_confirmation(self, transaction: MobileMoneyTransaction) -> bool:
        """Send payment confirmation SMS"""
        message = self.settings.payment_confirmed_template.format(
            course_title=transaction.course.title,
            reference_code=transaction.reference_code
        )
        
        return self._send_sms(
            transaction=transaction,
            phone_number=transaction.phone_number,
            message=message,
            notification_type='payment_confirmed'
        )
    
    def send_payment_reminder(self, transaction: MobileMoneyTransaction) -> bool:
        """Send payment reminder SMS"""
        message = f"Reminder: Complete your payment of {transaction.amount} {transaction.currency} " \
                 f"for {transaction.course.title}. Reference: {transaction.reference_code}. " \
                 f"Payment expires in 30 minutes."
        
        return self._send_sms(
            transaction=transaction,
            phone_number=transaction.phone_number,
            message=message,
            notification_type='payment_reminder'
        )
    
    def _send_sms(self, transaction: MobileMoneyTransaction, phone_number: str, 
                  message: str, notification_type: str) -> bool:
        """Send SMS using configured provider"""
        try:
            # Create SMS notification record
            sms_notification = SMSNotification.objects.create(
                transaction=transaction,
                phone_number=phone_number,
                message=message,
                notification_type=notification_type
            )
            
            # Here you would integrate with actual SMS provider
            # For now, we'll simulate successful sending
            sms_notification.delivered = True
            sms_notification.delivery_status = 'delivered'
            sms_notification.save()
            
            return True
            
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False

class PaymentProcessor:
    """Handle payment processing and enrollment"""
    
    def __init__(self):
        self.sms_service = SMSService()
    
    def initiate_payment(self, user, course, provider_name: str, phone_number: str) -> MobileMoneyTransaction:
        """Initiate a new mobile money payment"""
        
        # Validate phone number and detect provider
        detected_provider = PhoneNumberValidator.detect_provider(phone_number)
        if detected_provider != provider_name:
            raise ValueError(f"Phone number doesn't match {provider_name} network")
        
        # Get provider
        try:
            provider = MobileMoneyProvider.objects.get(name=provider_name, is_active=True)
        except MobileMoneyProvider.DoesNotExist:
            raise ValueError(f"Provider {provider_name} not available")
        
        # Create transaction
        transaction = MobileMoneyTransaction.objects.create(
            user=user,
            course=course,
            provider=provider,
            phone_number=PhoneNumberValidator.format_phone_number(phone_number),
            amount=course.price,
            currency='ZMW',
            status='initiated'
        )
        
        # Send payment instructions
        self.sms_service.send_payment_instructions(transaction)
        
        # Update status to pending
        transaction.status = 'pending'
        transaction.save()
        
        return transaction
    
    def confirm_payment(self, transaction: MobileMoneyTransaction, 
                       verification_method: str = 'manual', 
                       verified_by=None, notes: str = '') -> bool:
        """Confirm payment and create enrollment"""
        
        if transaction.status != 'pending':
            return False
        
        # Update transaction status
        transaction.status = 'confirmed'
        transaction.confirmed_at = timezone.now()
        transaction.save()
        
        # Create verification record
        from .models import PaymentVerification
        PaymentVerification.objects.create(
            transaction=transaction,
            method=verification_method,
            verified_by=verified_by,
            is_successful=True,
            notes=notes
        )
        
        # Create course enrollment
        enrollment, created = Enrollment.objects.get_or_create(
            user=transaction.user,
            course=transaction.course,
            defaults={
                'amount_paid': transaction.amount,
                'payment_status': 'completed',
                'payment_method': 'mobile_money'
            }
        )
        
        # Send confirmation SMS
        self.sms_service.send_payment_confirmation(transaction)
        
        return True
    
    def expire_pending_payments(self):
        """Mark expired payments as expired"""
        expired_transactions = MobileMoneyTransaction.objects.filter(
            status='pending',
            expires_at__lt=timezone.now()
        )
        
        expired_count = expired_transactions.update(status='expired')
        return expired_count

class PaymentStatusTracker:
    """Track and update payment statuses"""
    
    @staticmethod
    def get_transaction_status(reference_code: str) -> Dict[str, Any]:
        """Get current status of a transaction"""
        try:
            transaction = MobileMoneyTransaction.objects.get(reference_code=reference_code)
            
            return {
                'reference_code': transaction.reference_code,
                'status': transaction.status,
                'amount': float(transaction.amount),
                'currency': transaction.currency,
                'provider': transaction.provider.display_name,
                'course_title': transaction.course.title,
                'expires_at': transaction.expires_at.isoformat(),
                'is_expired': transaction.is_expired,
                'created_at': transaction.created_at.isoformat()
            }
            
        except MobileMoneyTransaction.DoesNotExist:
            return {'error': 'Transaction not found'}
    
    @staticmethod
    def update_from_sms(sms_content: str, sender_phone: str) -> bool:
        """Update transaction status from SMS confirmation"""
        # This would parse SMS confirmations from mobile money providers
        # Implementation depends on SMS format from each provider
        
        # Example SMS parsing logic
        reference_match = re.search(r'Reference[:\s]+(\d{8})', sms_content, re.IGNORECASE)
        if not reference_match:
            return False
        
        reference_code = reference_match.group(1)
        
        try:
            transaction = MobileMoneyTransaction.objects.get(
                reference_code=reference_code,
                status='pending'
            )
            
            # Check if SMS indicates successful payment
            success_keywords = ['successful', 'confirmed', 'completed', 'received']
            is_successful = any(keyword in sms_content.lower() for keyword in success_keywords)
            
            if is_successful:
                processor = PaymentProcessor()
                return processor.confirm_payment(
                    transaction=transaction,
                    verification_method='sms',
                    notes=f"SMS confirmation: {sms_content[:100]}"
                )
            
        except MobileMoneyTransaction.DoesNotExist:
            pass
        
        return False
