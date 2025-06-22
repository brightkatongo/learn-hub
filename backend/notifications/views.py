from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationPreference, Announcement
from .serializers import NotificationSerializer, NotificationPreferenceSerializer, AnnouncementSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def perform_update(self, serializer):
        # Mark as read when accessed
        if not serializer.instance.is_read:
            serializer.save(is_read=True, read_at=timezone.now())
        else:
            serializer.save()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, 
            recipient=request.user
        )
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    return Response({'message': 'All notifications marked as read'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications_count(request):
    count = Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).count()
    
    return Response({'unread_count': count})

class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference

class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        queryset = Announcement.objects.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        # Filter by target users or user types
        queryset = queryset.filter(
            models.Q(target_users=user) | 
            models.Q(target_users__isnull=True) |
            models.Q(target_user_types__contains=[user.user_type])
        ).distinct()
        
        return queryset

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_notification(request):
    """Send a notification to specific users (admin only)"""
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    recipient_ids = request.data.get('recipient_ids', [])
    title = request.data.get('title')
    message = request.data.get('message')
    notification_type = request.data.get('notification_type', 'system_announcement')
    
    if not recipient_ids or not title or not message:
        return Response(
            {'error': 'recipient_ids, title, and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    recipients = User.objects.filter(id__in=recipient_ids)
    notifications = []
    
    for recipient in recipients:
        notification = Notification.objects.create(
            recipient=recipient,
            sender=request.user,
            notification_type=notification_type,
            title=title,
            message=message
        )
        notifications.append(notification)
    
    return Response({
        'message': f'Sent {len(notifications)} notifications',
        'notification_ids': [str(n.id) for n in notifications]
    })
