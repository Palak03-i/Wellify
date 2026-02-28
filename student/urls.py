from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('chatbot/', views.chatbot_view, name='chatbot'),   # 👈 ADD THIS
    path('chatbot/send/', views.chatbot_send, name='chatbot_send'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('assessment/result/', views.assessment_result_view, name='assessment_result'),
    path('book/', views.book_session_view, name='book_session'),
]
