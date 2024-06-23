from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.view_notifications, name='view_notifications'),
    path('notifications/', views.get_notifications, name='notifications'),
    
]
