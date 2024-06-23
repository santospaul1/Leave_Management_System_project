# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, read=False).order_by('-timestamp')
    notification_data = [{'message': n.message, 'timestamp': n.timestamp} for n in notifications]
    return JsonResponse(notification_data, safe=False) 

@login_required
def view_notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/view_notifications.html', {'notifications': user_notifications})


