from django.urls import path
from . import views
from .views import add_leave_type, approved_leaves, declined_leaves, leave_type_list, leave_type_section, leaves_history, pending_leaves, update_leave_type

app_name = 'leave'

urlpatterns = [
    path('', leave_type_list, name='leavetype_list'),
    path('add_leave_type/', add_leave_type, name='add_leave_type'),
    path('approved-leaves/', approved_leaves, name='approved_leaves'),
    path('employee-leave-details/<int:leave_id>/', views.employee_leave_details, name='employee_leave_details'),
    path('declined-leaves/', declined_leaves, name='declined_leaves'),
    path('update_leave_type/<int:lid>/', views.update_leave_type, name='update_leave_type'),
    path('leaves_history/', leaves_history, name='leave_history'),
    path('pending_leaves/', pending_leaves, name='pending_leaves'),
    path('leave_type_list/', leave_type_list, name='leave_type_section'),
    path('leave_deleter/',leave_type_section, name='leave_deleter'),

]