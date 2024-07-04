from django.urls import path
from . import views

urlpatterns = [
    path('', views.provide_feedback, name='provide_feedback'),
    path('feedback_list/', views.feedback_list, name='feedback_list'),
    path('thank_you/', views.thank_you, name='thank_you'),
]
