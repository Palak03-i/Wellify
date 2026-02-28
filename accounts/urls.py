from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("redirect/", views.role_redirect_view, name="role_redirect"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("counsellor/", views.counsellor_dashboard, name="counsellor_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
