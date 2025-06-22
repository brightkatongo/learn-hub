from django.core.management.base import BaseCommand
from mobile_payments.services import PaymentProcessor

class Command(BaseCommand):
    help = 'Mark expired payments as expired'
    
    def handle(self, *args, **options):
        processor = PaymentProcessor()
        expired_count = processor.expire_pending_payments()
        
        self.stdout.write(
            self.style.SUCCESS(f'Marked {expired_count} payments as expired')
        )
