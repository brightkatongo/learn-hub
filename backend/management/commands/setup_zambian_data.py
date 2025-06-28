#!/usr/bin/env python3
"""
Setup script for Zambian education data
Run this to populate the database with Zambian education system data
"""

import os
import sys
import django
from datetime import date, datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnhub.settings')
django.setup()

from django.core.management.base import BaseCommand
from zambian_education.models import Province, District, Grade, Subject, AcademicYear
from ecz_papers.models import ECZExaminationSession

class Command(BaseCommand):
    help = 'Set up Zambian education system data'
    
    def handle(self, *args, **options):
        self.stdout.write('🇿🇲 Setting up Zambian Education System Data...')
        self.stdout.write('=' * 60)
        
        self.setup_provinces()
        self.setup_districts()
        self.setup_grades()
        self.setup_subjects()
        self.setup_academic_year()
        self.setup_ecz_sessions()
        
        self.stdout.write()
        self.stdout.write('=' * 60)
        self.stdout.write('✅ Zambian education system setup completed!')
        self.stdout.write()
        self.stdout.write('Next steps:')
        self.stdout.write('1. Run: python manage.py migrate')
        self.stdout.write('2. Run: python manage.py createsuperuser')
        self.stdout.write('3. Access admin at: /admin/dashboard/')
    
    def setup_provinces(self):
        """Set up Zambian provinces"""
        provinces_data = [
            {'name': 'lusaka', 'capital': 'Lusaka', 'population': 2191225, 'area_km2': 21896},
            {'name': 'copperbelt', 'capital': 'Ndola', 'population': 1972317, 'area_km2': 31328},
            {'name': 'southern', 'capital': 'Livingstone', 'population': 1589926, 'area_km2': 85823},
            {'name': 'eastern', 'capital': 'Chipata', 'population': 1592661, 'area_km2': 69106},
            {'name': 'central', 'capital': 'Kabwe', 'population': 1307560, 'area_km2': 94394},
            {'name': 'northern', 'capital': 'Kasama', 'population': 1105824, 'area_km2': 147826},
            {'name': 'western', 'capital': 'Mongu', 'population': 902974, 'area_km2': 126386},
            {'name': 'luapula', 'capital': 'Mansa', 'population': 991927, 'area_km2': 50567},
            {'name': 'northwestern', 'capital': 'Solwezi', 'population': 727044, 'area_km2': 125826},
            {'name': 'muchinga', 'capital': 'Chinsali', 'population': 711657, 'area_km2': 87806},
        ]
        
        for province_data in provinces_data:
            province, created = Province.objects.get_or_create(
                name=province_data['name'],
                defaults=province_data
            )
            
            if created:
                self.stdout.write(f'✅ Created province: {province.get_name_display()}')
            else:
                self.stdout.write(f'⚠️  Province already exists: {province.get_name_display()}')
    
    def setup_districts(self):
        """Set up major districts"""
        # This is a simplified list - in reality, Zambia has 116 districts
        districts_data = [
            # Lusaka Province
            ('lusaka', [
                ('Lusaka', 2191225),
                ('Kafue', 250000),
                ('Chongwe', 200000),
            ]),
            # Copperbelt Province
            ('copperbelt', [
                ('Ndola', 627503),
                ('Kitwe', 517543),
                ('Mufulira', 151309),
                ('Luanshya', 156059),
            ]),
            # Add more districts as needed
        ]
        
        for province_name, districts in districts_data:
            try:
                province = Province.objects.get(name=province_name)
                for district_name, population in districts:
                    district, created = District.objects.get_or_create(
                        province=province,
                        name=district_name,
                        defaults={'population': population}
                    )
                    
                    if created:
                        self.stdout.write(f'✅ Created district: {district_name}, {province.get_name_display()}')
            except Province.DoesNotExist:
                self.stdout.write(f'❌ Province {province_name} not found')
    
    def setup_grades(self):
        """Set up Zambian education grades"""
        grades_data = [
            # Primary Education
            ('grade_1', 'primary', 'Grade 1 - Foundation literacy and numeracy', 6, 7, False),
            ('grade_2', 'primary', 'Grade 2 - Building basic skills', 7, 8, False),
            ('grade_3', 'primary', 'Grade 3 - Developing reading and writing', 8, 9, False),
            ('grade_4', 'primary', 'Grade 4 - Intermediate primary education', 9, 10, False),
            ('grade_5', 'primary', 'Grade 5 - Advanced primary skills', 10, 11, False),
            ('grade_6', 'primary', 'Grade 6 - Pre-examination preparation', 11, 12, False),
            ('grade_7', 'primary', 'Grade 7 - Primary School Leaving Examination', 12, 13, True),
            
            # Junior Secondary
            ('grade_8', 'junior_secondary', 'Grade 8 - Introduction to secondary education', 13, 14, False),
            ('grade_9', 'junior_secondary', 'Grade 9 - Junior Secondary School Examination', 14, 15, True),
            
            # Senior Secondary
            ('grade_10', 'senior_secondary', 'Grade 10 - Senior secondary foundation', 15, 16, False),
            ('grade_11', 'senior_secondary', 'Grade 11 - Advanced secondary education', 16, 17, False),
            ('grade_12', 'senior_secondary', 'Grade 12 - School Certificate Examination', 17, 18, True),
        ]
        
        for level, phase, description, age_min, age_max, has_ecz in grades_data:
            grade, created = Grade.objects.get_or_create(
                level=level,
                defaults={
                    'phase': phase,
                    'description': description,
                    'typical_age_min': age_min,
                    'typical_age_max': age_max,
                    'has_ecz_exam': has_ecz,
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created grade: {grade.get_level_display()}')
    
    def setup_subjects(self):
        """Set up Zambian curriculum subjects"""
        subjects_data = [
            # Core subjects for all levels
            ('English', 'ENG', 'core', True, '001', 'English Language and Literature'),
            ('Mathematics', 'MATH', 'core', True, '002', 'Mathematics and Numeracy'),
            ('Science', 'SCI', 'core', True, '003', 'Integrated Science'),
            ('Social Studies', 'SS', 'core', False, '004', 'Social Studies and Civic Education'),
            
            # Secondary subjects
            ('Physics', 'PHY', 'core', True, '005', 'Physics'),
            ('Chemistry', 'CHEM', 'core', True, '006', 'Chemistry'),
            ('Biology', 'BIO', 'core', True, '007', 'Biology'),
            ('Geography', 'GEO', 'optional', True, '008', 'Geography'),
            ('History', 'HIST', 'optional', True, '009', 'History'),
            ('Civic Education', 'CE', 'core', True, '010', 'Civic Education'),
            ('Religious Education', 'RE', 'optional', True, '011', 'Religious Education'),
            ('Computer Studies', 'CS', 'optional', True, '012', 'Computer Studies and ICT'),
            ('Business Studies', 'BS', 'optional', True, '013', 'Business Studies'),
            ('Accounting', 'ACC', 'optional', True, '014', 'Principles of Accounts'),
            ('Economics', 'ECON', 'optional', True, '015', 'Economics'),
            
            # Practical subjects
            ('Creative Arts', 'CA', 'practical', False, '016', 'Creative and Performing Arts'),
            ('Physical Education', 'PE', 'practical', False, '017', 'Physical Education and Sports'),
            ('Home Economics', 'HE', 'practical', False, '018', 'Home Economics'),
            ('Design and Technology', 'DT', 'practical', False, '019', 'Design and Technology'),
            
            # Languages
            ('Bemba', 'BEM', 'language', False, '020', 'Bemba Language'),
            ('Nyanja', 'NYA', 'language', False, '021', 'Nyanja Language'),
            ('Tonga', 'TON', 'language', False, '022', 'Tonga Language'),
            ('Lozi', 'LOZ', 'language', False, '023', 'Lozi Language'),
        ]
        
        for name, code, category, is_ecz, ecz_code, description in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'category': category,
                    'description': description,
                    'is_ecz_subject': is_ecz,
                    'ecz_subject_code': ecz_code if is_ecz else '',
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created subject: {name} ({code})')
                
                # Assign subjects to appropriate grades
                if category in ['core', 'practical', 'language']:
                    # Primary subjects
                    primary_grades = Grade.objects.filter(phase='primary')
                    subject.grades.add(*primary_grades)
                
                if category in ['core', 'optional']:
                    # Secondary subjects
                    secondary_grades = Grade.objects.filter(phase__in=['junior_secondary', 'senior_secondary'])
                    subject.grades.add(*secondary_grades)
    
    def setup_academic_year(self):
        """Set up current academic year"""
        current_year = datetime.now().year
        
        academic_year, created = AcademicYear.objects.get_or_create(
            year=current_year,
            defaults={
                'start_date': date(current_year, 1, 15),
                'end_date': date(current_year, 12, 15),
                'term_1_start': date(current_year, 1, 15),
                'term_1_end': date(current_year, 4, 15),
                'term_2_start': date(current_year, 5, 1),
                'term_2_end': date(current_year, 8, 15),
                'term_3_start': date(current_year, 9, 1),
                'term_3_end': date(current_year, 12, 15),
                'is_current': True,
            }
        )
        
        if created:
            self.stdout.write(f'✅ Created academic year: {current_year}')
    
    def setup_ecz_sessions(self):
        """Set up ECZ examination sessions"""
        current_year = datetime.now().year
        
        sessions_data = [
            ('grade_7', 'october', date(current_year, 6, 1), date(current_year, 7, 31), 
             date(current_year, 10, 15), date(current_year, 10, 25), 150.00, 200.00),
            ('grade_9', 'october', date(current_year, 6, 1), date(current_year, 7, 31),
             date(current_year, 11, 1), date(current_year, 11, 15), 200.00, 250.00),
            ('grade_12', 'october', date(current_year, 6, 1), date(current_year, 7, 31),
             date(current_year, 11, 20), date(current_year, 12, 10), 300.00, 400.00),
        ]
        
        for exam_type, session, reg_start, reg_end, exam_start, exam_end, reg_fee, late_fee in sessions_data:
            ecz_session, created = ECZExaminationSession.objects.get_or_create(
                year=current_year,
                session=session,
                examination_type=exam_type,
                defaults={
                    'registration_start': reg_start,
                    'registration_end': reg_end,
                    'examination_start': exam_start,
                    'examination_end': exam_end,
                    'registration_fee': reg_fee,
                    'late_registration_fee': late_fee,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created ECZ session: {exam_type} {session} {current_year}')

if __name__ == '__main__':
    command = Command()
    command.handle()