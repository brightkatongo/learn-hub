from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import json

from .models import MobileMoneyTransaction, MobileMoneyProvider
from .serializers import (
    MobileMoneyTransactionSerializer, 
    PaymentInitiationSerializer,
    MobileMoneyProviderSerializer
)
from .services import (
    PaymentProcessor, 
    USSDInstructionGenerator, 
    PaymentStatusTracker,
    PhoneNumberValidator
)
from courses.models import Course

class MobileMoneyProviderListView(generics.ListAPIView):
    """List available mobile money providers"""
    queryset = MobileMoneyProvider.objects.filter(is_active=True)
    serializer_class = MobileMoneyProviderSerializer
    permission_classes = [permissions.AllowAny]

class MobileMoneyTransactionListView(generics.ListAPIView):
    """List user's mobile money transactions"""
    serializer_class = MobileMoneyTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MobileMoneyTransaction.objects.filter(user=self.request.user)

class MobileMoneyTransactionDetailView(generics.RetrieveAPIView):
    """Get transaction details"""
    serializer_class = MobileMoneyTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'reference_code'
    
    def get_queryset(self):
        return MobileMoneyTransaction.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_payment(request):
    """Initiate a mobile money payment"""
    serializer = PaymentInitiationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
        provider_name = serializer.validated_data['provider']
        phone_number = serializer.validated_data['phone_number']
        
        # Check if user is already enrolled
        from courses.models import Enrollment
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for existing pending payment
        existing_payment = MobileMoneyTransaction.objects.filter(
            user=request.user,
            course=course,
            status__in=['initiated', 'pending']
        ).first()
        
        if existing_payment and not existing_payment.is_expired:
            return Response({
                'message': 'Payment already in progress',
                'transaction': MobileMoneyTransactionSerializer(existing_payment).data
            })
        
        # Initiate new payment
        processor = PaymentProcessor()
        transaction = processor.initiate_payment(
            user=request.user,
            course=course,
            provider_name=provider_name,
            phone_number=phone_number
        )
        
        # Get USSD instructions
        instructions = USSDInstructionGenerator.get_instructions(provider_name, transaction)
        
        return Response({
            'transaction': MobileMoneyTransactionSerializer(transaction).data,
            'instructions': instructions,
            'message': 'Payment initiated successfully. Follow the USSD instructions to complete payment.'
        })
        
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': 'Payment initiation failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_status(request, reference_code):
    """Get payment status"""
    transaction_status = PaymentStatusTracker.get_transaction_status(reference_code)
    
    if 'error' in transaction_status:
        return Response(transaction_status, status=status.HTTP_404_NOT_FOUND)
    
    return Response(transaction_status)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_payment(request, reference_code):
    """Cancel a pending payment"""
    try:
        transaction = MobileMoneyTransaction.objects.get(
            reference_code=reference_code,
            user=request.user,
            status__in=['initiated', 'pending']
        )
        
        transaction.status = 'cancelled'
        transaction.save()
        
        return Response({'message': 'Payment cancelled successfully'})
        
    except MobileMoneyTransaction.DoesNotExist:
        return Response(
            {'error': 'Transaction not found or cannot be cancelled'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def validate_phone_number(request):
    """Validate phone number and detect provider"""
    phone_number = request.data.get('phone_number')
    
    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        clean_phone = PhoneNumberValidator.clean_phone_number(phone_number)
        formatted_phone = PhoneNumberValidator.format_phone_number(phone_number)
        detected_provider = PhoneNumberValidator.detect_provider(phone_number)
        
        return Response({
            'is_valid': len(clean_phone) == 9,
            'formatted_phone': formatted_phone,
            'detected_provider': detected_provider,
            'clean_phone': clean_phone
        })
        
    except Exception as e:
        return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sms_webhook(request):
    """Handle SMS confirmations from mobile money providers"""
    try:
        # Parse webhook data (format depends on SMS provider)
        data = json.loads(request.body) if request.body else request.POST
        
        sms_content = data.get('message', '')
        sender_phone = data.get('from', '')
        
        if not sms_content:
            return JsonResponse({'error': 'No message content'}, status=400)
        
        # Update transaction status from SMS
        success = PaymentStatusTracker.update_from_sms(sms_content, sender_phone)
        
        return JsonResponse({
            'success': success,
            'message': 'SMS processed successfully' if success else 'No matching transaction found'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_instructions(request, reference_code):
    """Get detailed payment instructions for a transaction"""
    try:
        transaction = MobileMoneyTransaction.objects.get(
            reference_code=reference_code,
            user=request.user
        )
        
        instructions = USSDInstructionGenerator.get_instructions(
            transaction.provider.name, 
            transaction
        )
        
        return Response({
            'transaction': MobileMoneyTransactionSerializer(transaction).data,
            'instructions': instructions,
            'qr_code_data': f"tel:{instructions.get('ussd_code', '')}"
        })
        
    except MobileMoneyTransaction.DoesNotExist:
        return Response(
            {'error': 'Transaction not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
