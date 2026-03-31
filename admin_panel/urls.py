from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('reports/', views.reports_view, name='reports'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    # ERP/LMS Integration - Disabled (Coming Soon)
    # path('erp/', views.erp_integration, name='erp_integration'),
    # Disabled for VIEW-ONLY mode
    # path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    # path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    # path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
