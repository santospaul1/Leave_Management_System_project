from django.urls import path
from . import views
from .views import  add_employee, employees, update_employee, view_employee

app_name = 'employee'

urlpatterns = [
    path('', employees, name='employees'),
    path('add_employee/', add_employee, name='add_employee'),
    
    path('update_employee/<str:empcode>/', update_employee, name='update_employee'),
    path('view_employee/<str:empcode>/', view_employee, name='view_employee'),
    #path('employee-leave-details/<int:leave_id>/', employee_leave_details, name='employee_leave_details'),
    path('delete_employee/', views.delete_employee, name='delete_employee'),
    path('update_profile/<str:empcode>/', views.update_profile, name='update_profile'),
    path('logout/', views.logout, name='logout'),
    


]