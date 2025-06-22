from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('', views.CourseListView.as_view(), name='course-list'),
    path('<uuid:id>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('featured/', views.featured_courses, name='featured-courses'),
    path('popular/', views.popular_courses, name='popular-courses'),
    path('search/', views.course_search, name='course-search'),
    
    # Student endpoints
    path('enroll/<uuid:course_id>/', views.enroll_course, name='enroll-course'),
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<uuid:id>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enrollments/<uuid:enrollment_id>/lectures/<uuid:lecture_id>/progress/', 
         views.LectureProgressView.as_view(), name='lecture-progress'),
    
    # Reviews
    path('<uuid:course_id>/reviews/', views.ReviewListCreateView.as_view(), name='course-reviews'),
    
    # Instructor endpoints
    path('instructor/courses/', views.InstructorCourseListView.as_view(), name='instructor-courses'),
    path('instructor/courses/<uuid:id>/', views.InstructorCourseDetailView.as_view(), name='instructor-course-detail'),
    path('instructor/courses/<uuid:course_id>/sections/', views.SectionListCreateView.as_view(), name='course-sections'),
    path('instructor/sections/<int:section_id>/lectures/', views.LectureListCreateView.as_view(), name='section-lectures'),
]
