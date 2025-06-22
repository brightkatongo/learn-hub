from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/details/', views.UserProfileDetailView.as_view(), name='user-profile-details'),
    path('instructor/profile/', views.InstructorProfileView.as_view(), name='instructor-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('dashboard/stats/', views.user_dashboard_stats, name='dashboard-stats'),
]
