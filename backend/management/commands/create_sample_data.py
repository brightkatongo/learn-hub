from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import UserProfile, InstructorProfile
from courses.models import Category, Course, Enrollment
from dashboard.models import SystemMetrics
from mobile_payments.models import MobileMoneyProvider

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing the admin dashboard'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample categories and courses
        self.create_sample_courses()
        
        # Create sample enrollments
        self.create_sample_enrollments()
        
        # Create sample metrics
        self.create_sample_metrics()
        
        # Setup mobile money providers
        self.setup_mobile_providers()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
    
    def create_sample_users(self):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            email='admin@learnhub.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.create(user=admin_user)
        
        # Create sample instructors
        instructors_data = [
            {
                'email': 'sarah.johnson@learnhub.com',
                'username': 'sarah_johnson',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'bio': 'Senior Full Stack Developer with 8+ years experience',
                'country': 'Zambia',
                'city': 'Lusaka'
            },
            {
                'email': 'michael.chen@learnhub.com',
                'username': 'michael_chen',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'bio': 'Data Science Expert and Machine Learning Specialist',
                'country': 'South Africa',
                'city': 'Cape Town'
            },
            {
                'email': 'emma.rodriguez@learnhub.com',
                'username': 'emma_rodriguez',
                'first_name': 'Emma',
                'last_name': 'Rodriguez',
                'bio': 'UI/UX Designer with focus on user-centered design',
                'country': 'Kenya',
                'city': 'Nairobi'
            }
        ]
        
        for instructor_data in instructors_data:
            user, created = User.objects.get_or_create(
                email=instructor_data['email'],
                defaults={
                    **instructor_data,
                    'user_type': 'instructor',
                    'is_verified': True,
                    'login_count': random.randint(10, 100),
                }
            )
            if created:
                user.set_password('instructor123')
                user.save()
                
                UserProfile.objects.create(
                    user=user,
                    total_courses_completed=random.randint(5, 20),
                    total_learning_hours=random.randint(100, 500),
                    current_streak_days=random.randint(1, 30)
                )
                
                InstructorProfile.objects.create(
                    user=user,
                    experience_years=random.randint(3, 15),
                    is_approved=True,
                    approval_date=timezone.now(),
                    approved_by=admin_user,
                    total_students=random.randint(100, 1000),
                    total_courses=random.randint(2, 10),
                    average_rating=round(random.uniform(4.0, 5.0), 2),
                    hourly_rate=random.randint(25, 100)
                )
        
        # Create sample students
        for i in range(50):
            user, created = User.objects.get_or_create(
                email=f'student{i+1}@example.com',
                defaults={
                    'username': f'student{i+1}',
                    'first_name': f'Student',
                    'last_name': f'{i+1}',
                    'user_type': 'student',
                    'is_verified': random.choice([True, False]),
                    'login_count': random.randint(1, 50),
                    'country': random.choice(['Zambia', 'South Africa', 'Kenya', 'Nigeria']),
                    'city': random.choice(['Lusaka', 'Cape Town', 'Nairobi', 'Lagos'])
                }
            )
            if created:
                user.set_password('student123')
                user.save()
                
                UserProfile.objects.create(
                    user=user,
                    total_courses_completed=random.randint(0, 10),
                    total_learning_hours=random.randint(0, 200),
                    current_streak_days=random.randint(0, 15)
                )
    
    def create_sample_courses(self):
        # Create categories
        categories_data = [
            {'name': 'Web Development', 'description': 'Learn web development technologies'},
            {'name': 'Data Science', 'description': 'Master data analysis and machine learning'},
            {'name': 'Design', 'description': 'UI/UX and graphic design courses'},
            {'name': 'Business', 'description': 'Business and entrepreneurship skills'},
            {'name': 'Marketing', 'description': 'Digital marketing and growth strategies'},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': cat_data['name'].lower().replace(' ', '-')
                }
            )
        
        # Create sample courses
        instructors = User.objects.filter(user_type='instructor')
        categories = Category.objects.all()
        
        courses_data = [
            {
                'title': 'Complete React Developer Course',
                'subtitle': 'Learn React from scratch and build amazing web applications',
                'description': 'This comprehensive React course will take you from beginner to advanced level.',
                'price': 89.99,
                'difficulty_level': 'beginner',
                'status': 'published'
            },
            {
                'title': 'Machine Learning Masterclass',
                'subtitle': 'Master machine learning algorithms and build intelligent systems',
                'description': 'Learn machine learning from basics to advanced concepts.',
                'price': 129.99,
                'difficulty_level': 'intermediate',
                'status': 'published'
            },
            {
                'title': 'UI/UX Design Fundamentals',
                'subtitle': 'Create beautiful and user-friendly interfaces',
                'description': 'Learn the principles of good design and user experience.',
                'price': 69.99,
                'difficulty_level': 'beginner',
                'status': 'published'
            },
            {
                'title': 'Digital Marketing Strategy',
                'subtitle': 'Master digital marketing techniques and grow your business',
                'description': 'Learn effective digital marketing strategies.',
                'price': 79.99,
                'difficulty_level': 'beginner',
                'status': 'published'
            },
            {
                'title': 'Python for Data Science',
                'subtitle': 'Learn Python programming for data analysis',
                'description': 'Master Python for data science applications.',
                'price': 99.99,
                'difficulty_level': 'intermediate',
                'status': 'published'
            }
        ]
        
        for course_data in courses_data:
            Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    **course_data,
                    'instructor': random.choice(instructors),
                    'category': random.choice(categories),
                    'total_duration': random.randint(1200, 3600),  # 20-60 hours
                    'total_lectures': random.randint(20, 100),
                    'is_featured': random.choice([True, False]),
                    'is_bestseller': random.choice([True, False]),
                }
            )
    
    def create_sample_enrollments(self):
        students = User.objects.filter(user_type='student')
        courses = Course.objects.filter(status='published')
        
        # Create random enrollments
        for _ in range(200):
            student = random.choice(students)
            course = random.choice(courses)
            
            enrollment, created = Enrollment.objects.get_or_create(
                user=student,
                course=course,
                defaults={
                    'amount_paid': course.price,
                    'payment_status': random.choice(['completed', 'pending', 'failed']),
                    'progress_percentage': random.randint(0, 100),
                    'completed': random.choice([True, False]),
                    'enrolled_at': timezone.now() - timedelta(days=random.randint(1, 365))
                }
            )
    
    def create_sample_metrics(self):
        # Create metrics for the last 30 days
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            
            SystemMetrics.objects.get_or_create(
                date=date,
                defaults={
                    'total_users': 1000 + i * 10,
                    'new_users_today': random.randint(5, 25),
                    'active_users_today': random.randint(50, 200),
                    'total_courses': 50 + i,
                    'new_courses_today': random.randint(0, 3),
                    'published_courses': 45 + i,
                    'total_enrollments': 500 + i * 20,
                    'new_enrollments_today': random.randint(10, 50),
                    'completed_courses_today': random.randint(5, 20),
                    'total_revenue': 10000 + i * 500,
                    'revenue_today': random.randint(200, 1000),
                    'mobile_payments_today': random.randint(5, 30),
                    'mobile_revenue_today': random.randint(100, 500),
                }
            )
    
    def setup_mobile_providers(self):
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
            MobileMoneyProvider.objects.get_or_create(
                name=provider_data['name'],
                defaults=provider_data
            )