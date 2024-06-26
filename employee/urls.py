from django.urls import path
from . import views
from .views import add_employee, employees, update_employee, view_employee, change_password, view_employee_leaves

app_name = 'employee'

urlpatterns = [
    path('', employees, name='employees'),
    path('add_employee/', add_employee, name='add_employee'),
    path('update_employee/<str:empcode>/', update_employee, name='update_employee'),
    path('view_employee/<str:empcode>/', view_employee, name='view_employee'),
    path('view_employee_leaves/<str:empcode>/', view_employee_leaves, name='view_employee_leaves'),
    path('delete_employee/', views.delete_employee, name='delete_employee'),
    path('update_profile/<str:empcode>/', views.update_profile, name='update_profile'),
    path('employee_profile/<str:empcode>/', views.employee_profile, name='employee_profile'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', views.logout, name='logout'),
    


]