"""
URL configuration for Leave_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from accounts.views import employee_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', employee_login, name='employee_login'),
    path("admin/", admin.site.urls),
    path('', include('accounts.urls')),
    path('myadmin/', include('myadmin.urls')),
    path('employee/',include('employee.urls') ),
    path('department/', include('department.urls')),
    path('leave/', include('leave.urls')),
    path('holiday/', include('holiday.urls')),
    path('notification/', include('notification.urls')),
    path('feedback/', include('feedback.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)