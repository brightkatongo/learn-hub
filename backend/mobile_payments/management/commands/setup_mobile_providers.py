from django.core.management.base import BaseCommand
from mobile_payments.models import MobileMoneyProvider

class Command(BaseCommand):
    help = 'Set up mobile money providers for Zambia'
    
    def handle(self, *args, **options):
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
                'business_number': '2001',
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
                self.stdout.write(
                    self.style.SUCCESS(f'Created provider: {provider.display_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Provider already exists: {provider.display_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Mobile money providers setup completed!')
        )
