from rest_framework import serializers
from .models import Payment, Coupon, CouponUsage, InstructorPayout

class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'completed_at')

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ('used_count', 'created_at')

class CouponValidationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    course_id = serializers.UUIDField()
    
    def validate(self, attrs):
        from django.utils import timezone
        from courses.models import Course
        
        try:
            coupon = Coupon.objects.get(code=attrs['code'])
            course = Course.objects.get(id=attrs['course_id'])
        except (Coupon.DoesNotExist, Course.DoesNotExist):
            raise serializers.ValidationError("Invalid coupon or course")
        
        if not coupon.is_valid:
            raise serializers.ValidationError("Coupon is not valid or has expired")
        
        if coupon.applicable_courses.exists() and course not in coupon.applicable_courses.all():
            raise serializers.ValidationError("Coupon is not applicable to this course")
        
        if course.price < coupon.minimum_amount:
            raise serializers.ValidationError(f"Minimum purchase amount is ${coupon.minimum_amount}")
        
        attrs['coupon'] = coupon
        attrs['course'] = course
        return attrs

class InstructorPayoutSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    
    class Meta:
        model = InstructorPayout
        fields = '__all__'
        read_only_fields = ('id', 'instructor', 'created_at', 'processed_at')
