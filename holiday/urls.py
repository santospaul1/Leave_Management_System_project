
from django.urls import path
from .views import add_holiday, edit_holiday, holiday_list, delete_holiday

urlpatterns = [
    path('', holiday_list, name='holiday_list'),
    path('add_holiday', add_holiday, name='add_holiday'),
    path('holiday/edit/<int:holiday_id>/', edit_holiday, name='edit_holiday'),
    path('holidays/delete/<int:holiday_id>/', delete_holiday, name='delete_holiday'),
]
