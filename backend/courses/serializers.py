from rest_framework import serializers
from .models import (
    Category, Course, Section, Lecture, Enrollment, 
    LectureProgress, Review, Quiz, Question
)

class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_course_count(self, obj):
        return obj.courses.filter(status='published').count()

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class SectionSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)
    lecture_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = '__all__'
    
    def get_lecture_count(self, obj):
        return obj.lectures.count()
    
    def get_total_duration(self, obj):
        return sum([lecture.video_duration for lecture in obj.lectures.all()])

class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'subtitle', 'description', 'instructor_name', 
            'category_name', 'thumbnail', 'price', 'original_price', 'is_free',
            'difficulty_level', 'language', 'is_bestseller', 'is_featured',
            'total_duration', 'total_lectures', 'average_rating', 'total_students',
            'created_at', 'updated_at'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'published_at')
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', 'instructor', 'created_at', 'updated_at', 'published_at')
    
    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'enrolled_at', 'last_accessed')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class LectureProgressSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer(read_only=True)
    
    class Meta:
        model = LectureProgress
        fields = '__all__'
        read_only_fields = ('enrollment', 'created_at', 'updated_at')

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'
