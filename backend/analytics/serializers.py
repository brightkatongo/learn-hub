from rest_framework import serializers
from .models import UserActivity, CourseAnalytics, LearningPath, PlatformAnalytics

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')

class CourseAnalyticsSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CourseAnalytics
        fields = '__all__'

class LearningPathSerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()
    completed_courses = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningPath
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def get_courses_count(self, obj):
        return obj.courses.count()
    
    def get_completed_courses(self, obj):
        return obj.learningpathcourse_set.filter(completed=True).count()
    
    def get_progress_percentage(self, obj):
        total = obj.courses.count()
        completed = obj.learningpathcourse_set.filter(completed=True).count()
        return (completed / total * 100) if total > 0 else 0

class PlatformAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformAnalytics
        fields = '__all__'
