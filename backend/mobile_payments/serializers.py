from rest_framework import serializers
from .models import MobileMoneyTransaction, MobileMoneyProvider
from .services import PhoneNumberValidator

class MobileMoneyProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileMoneyProvider
        fields = ['name', 'display_name', 'ussd_code', 'phone_prefixes', 'instructions']

class MobileMoneyTransactionSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.display_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = MobileMoneyTransaction
        fields = [
            'id', 'reference_code', 'provider_name', 'course_title', 'user_email',
            'phone_number', 'amount', 'currency', 'status', 'is_expired',
            'expires_at', 'confirmed_at', 'created_at', 'failure_reason'
        ]
        read_only_fields = [
            'id', 'reference_code', 'expires_at', 'confirmed_at', 
            'created_at', 'is_expired'
        ]

class PaymentInitiationSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()
    provider = serializers.ChoiceField(choices=['airtel', 'zamtel', 'mtn'])
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        """Validate Zambian phone number format"""
        clean_phone = PhoneNumberValidator.clean_phone_number(value)
        
        if len(clean_phone) != 9:
            raise serializers.ValidationError("Invalid Zambian phone number format")
        
        return value
    
    def validate(self, attrs):
        """Validate that phone number matches selected provider"""
        phone_number = attrs['phone_number']
        provider = attrs['provider']
        
        detected_provider = PhoneNumberValidator.detect_provider(phone_number)
        
        if detected_provider != provider:
            raise serializers.ValidationError(
                f"Phone number doesn't match {provider} network. "
                f"Detected: {detected_provider or 'unknown'}"
            )
        
        return attrs
