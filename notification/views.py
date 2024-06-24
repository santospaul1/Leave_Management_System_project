# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
    notification_data = [{'message': n.message, 'timestamp': n.timestamp} for n in notifications]
    return JsonResponse(notification_data, safe=False) 


@login_required
def view_notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/view_notifications.html', {'user_notifications': user_notifications})

@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return render(request, 'notifications/notification_detail.html', {'notification': notification})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_detail')  # Redirect to a notifications page or any other page you prefer

@login_required
def fetch_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
    data = [{"id": notification.id, "message": notification.message, "url": reverse('mark_as_read', args=[notification.id])} for notification in notifications]
    return JsonResponse(data, safe=False)
