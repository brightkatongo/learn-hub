from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.UserActivityListView.as_view(), name='user-activities'),
    path('track/', views.track_activity, name='track-activity'),
    path('user/stats/', views.user_learning_stats, name='user-learning-stats'),
    path('instructor/stats/', views.instructor_analytics, name='instructor-analytics'),
    path('platform/stats/', views.platform_analytics, name='platform-analytics'),
    path('learning-paths/', views.LearningPathListCreateView.as_view(), name='learning-paths'),
    path('learning-paths/<int:pk>/', views.LearningPathDetailView.as_view(), name='learning-path-detail'),
]
