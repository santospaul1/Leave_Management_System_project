from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.view_notifications, name='view_notifications'),
    path('notifications/', views.get_notifications, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notification/', views.fetch_notifications, name='notification'),
    
]
