from django.urls import path
from . import views
from .views import add_department, department, update_department

app_name = 'department'

urlpatterns = [
    path('', department, name='department'),
    path('add_department/', add_department, name='add_department'),
    path('update_department/<int:deptid>/', update_department, name='update_department'),

]