from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
import stripe
from .models import Payment, Coupon, CouponUsage, InstructorPayout
from .serializers import PaymentSerializer, CouponSerializer, CouponValidationSerializer, InstructorPayoutSerializer
from courses.models import Course, Enrollment

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_payment_intent(request):
    try:
        course_id = request.data.get('course_id')
        coupon_code = request.data.get('coupon_code')
        
        course = Course.objects.get(id=course_id, status='published')
        
        # Check if already enrolled
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount = course.price
        discount_amount = 0
        coupon = None
        
        # Apply coupon if provided
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid and (not coupon.applicable_courses.exists() or course in coupon.applicable_courses.all()):
                    if coupon.discount_type == 'percentage':
                        discount_amount = (amount * coupon.discount_value) / 100
                        if coupon.maximum_discount:
                            discount_amount = min(discount_amount, coupon.maximum_discount)
                    else:
                        discount_amount = coupon.discount_value
                    
                    amount = max(0, amount - discount_amount)
            except Coupon.DoesNotExist:
                return Response(
                    {'error': 'Invalid coupon code'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe expects cents
            currency='usd',
            metadata={
                'course_id': str(course.id),
                'user_id': str(request.user.id),
                'coupon_code': coupon_code or '',
            }
        )
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            stripe_payment_intent_id=intent.id,
            payment_status='pending'
        )
        
        return Response({
            'client_secret': intent.client_secret,
            'payment_id': payment.id,
            'amount': amount,
            'discount_amount': discount_amount,
        })
        
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_payment(request):
    try:
        payment_intent_id = request.data.get('payment_intent_id')
        
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Update payment record
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            payment.payment_status = 'completed'
            payment.completed_at = timezone.now()
            payment.stripe_charge_id = intent.charges.data[0].id if intent.charges.data else None
            payment.save()
            
            # Create enrollment
            enrollment, created = Enrollment.objects.get_or_create(
                user=payment.user,
                course=payment.course,
                defaults={
                    'amount_paid': payment.amount,
                    'payment_status': 'completed'
                }
            )
            
            # Handle coupon usage
            coupon_code = intent.metadata.get('coupon_code')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=payment.user,
                        payment=payment,
                        discount_amount=payment.course.price - payment.amount
                    )
                    coupon.used_count += 1
                    coupon.save()
                except Coupon.DoesNotExist:
                    pass
            
            return Response({
                'message': 'Payment confirmed and enrollment created',
                'enrollment_id': enrollment.id
            })
        else:
            return Response(
                {'error': 'Payment not successful'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return Response(status=400)
    except stripe.error.SignatureVerificationError:
        return Response(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.payment_status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # Handle failed payment
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.payment_status = 'failed'
            payment.failure_reason = payment_intent.get('last_payment_error', {}).get('message', '')
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return Response(status=200)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def validate_coupon(request):
    serializer = CouponValidationSerializer(data=request.data)
    if serializer.is_valid():
        coupon = serializer.validated_data['coupon']
        course = serializer.validated_data['course']
        
        discount_amount = 0
        if coupon.discount_type == 'percentage':
            discount_amount = (course.price * coupon.discount_value) / 100
            if coupon.maximum_discount:
                discount_amount = min(discount_amount, coupon.maximum_discount)
        else:
            discount_amount = coupon.discount_value
        
        final_price = max(0, course.price - discount_amount)
        
        return Response({
            'valid': True,
            'discount_amount': discount_amount,
            'final_price': final_price,
            'discount_type': coupon.discount_type,
            'discount_value': coupon.discount_value,
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstructorPayoutListView(generics.ListAPIView):
    serializer_class = InstructorPayoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type != 'instructor':
            return InstructorPayout.objects.none()
        return InstructorPayout.objects.filter(instructor=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def instructor_earnings(request):
    if request.user.user_type != 'instructor':
        return Response(
            {'error': 'Only instructors can access this endpoint'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    from django.db.models import Sum
    from courses.models import Course
    
    courses = Course.objects.filter(instructor=request.user)
    total_revenue = sum([course.total_revenue for course in courses])
    instructor_share = total_revenue * 0.7  # 70% to instructor, 30% platform fee
    
    # Get pending payout amount
    pending_payout = InstructorPayout.objects.filter(
        instructor=request.user,
        payout_status='pending'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'total_revenue': total_revenue,
        'instructor_share': instructor_share,
        'pending_payout': pending_payout,
        'available_for_payout': instructor_share - pending_payout,
    })
