#!/usr/bin/env python3
"""
Setup script for mobile money payments
Run this after setting up the Django backend
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnhub.settings')
django.setup()

from mobile_payments.models import MobileMoneyProvider, PaymentSettings

def setup_providers():
    """Set up mobile money providers for Zambia"""
    providers_data = [
        {
            'name': 'airtel',
            'display_name': 'Airtel Money',
            'ussd_code': '*778#',
            'merchant_code': 'LEARNHUB001',
            'phone_prefixes': ['097', '096', '095'],
            'instructions': 'Dial *778# > Send Money > Pay Bill > Enter Merchant Code > Enter Amount > Enter Reference > Confirm with PIN'
        },
        {
            'name': 'zamtel',
            'display_name': 'Zamtel Money', 
            'ussd_code': '*776#',
            'business_number': '+260978230114',
            'phone_prefixes': ['095', '094'],
            'instructions': 'Dial *776# > Pay Bill > Enter Business Number > Enter Amount > Enter Reference > Confirm with PIN'
        },
        {
            'name': 'mtn',
            'display_name': 'MTN Money',
            'ussd_code': '*175#',
            'payee_code': 'LEARN001', 
            'phone_prefixes': ['096', '097', '098'],
            'instructions': 'Dial *175# > Send Money > Pay Bill > Enter Payee Code > Enter Amount > Enter Reference > Confirm with PIN'
        }
    ]
    
    for provider_data in providers_data:
        provider, created = MobileMoneyProvider.objects.get_or_create(
            name=provider_data['name'],
            defaults=provider_data
        )
        
        if created:
            print(f'✅ Created provider: {provider.display_name}')
        else:
            print(f'⚠️  Provider already exists: {provider.display_name}')

def setup_payment_settings():
    """Set up default payment settings"""
    settings, created = PaymentSettings.objects.get_or_create(
        id=1,
        defaults={
            'payment_timeout_minutes': 30,
            'max_payment_attempts': 3,
            'sms_provider': 'africas_talking',
            'auto_verification_enabled': False,
            'payment_instructions_template': 'Complete your payment of {amount} {currency} for {course_title}. Dial {ussd_code} and use reference: {reference_code}',
            'payment_confirmed_template': 'Payment confirmed! You now have access to {course_title}. Reference: {reference_code}'
        }
    )
    
    if created:
        print('✅ Created payment settings')
    else:
        print('⚠️  Payment settings already exist')

def main():
    """Main setup function"""
    print("🚀 Setting up mobile money payments for LearnHub...")
    print("=" * 50)
    
    setup_providers()
    print()
    setup_payment_settings()
    
    print()
    print("=" * 50)
    print("✅ Mobile money payment setup completed!")
    print()
    print("Next steps:")
    print("1. Run migrations: python manage.py migrate")
    print("2. Create superuser: python manage.py createsuperuser")
    print("3. Configure SMS provider settings")
    print("4. Test payment flow in admin panel")

if __name__ == '__main__':
    main()
