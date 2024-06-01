from django.urls import path

from myadmin.views import add_admin, admin_login, dashboard, manage_admin, user_logout



app_name = 'myadmin'

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('add_admin/', add_admin, name='add_admin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user_logout/', user_logout, name='user_logout'),
    path('manage-admin/', manage_admin, name='manage_admin'),

]