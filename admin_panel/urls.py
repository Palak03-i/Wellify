from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
]
