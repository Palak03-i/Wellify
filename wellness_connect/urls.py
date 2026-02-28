"""
Main URL configuration. Includes accounts, student, counsellor, admin_panel.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('student/', include('student.urls')),
    path('counsellor/', include('counsellor.urls')),
    path('admin_panel/', include('admin_panel.urls')),
]
