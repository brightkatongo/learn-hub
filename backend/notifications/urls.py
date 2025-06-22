from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:id>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('<uuid:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('unread-count/', views.unread_notifications_count, name='unread-notifications-count'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcements'),
    path('send/', views.send_notification, name='send-notification'),
]
