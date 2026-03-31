from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/send/', views.chatbot_send, name='chatbot_send'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('assessment/result/', views.assessment_result_view, name='assessment_result'),
    path('book/', views.book_session_view, name='book_session'),
    # Wellness Content
    path('meditation/', views.meditation_list, name='meditation_list'),
    path('meditation/<str:meditation_id>/', views.meditation_detail, name='meditation_detail'),
    path('breathing/', views.breathing_list, name='breathing_list'),
    path('breathing/<str:breathing_id>/', views.breathing_detail, name='breathing_detail'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/create/', views.journal_create, name='journal_create'),
    path('journal/<str:journal_id>/', views.journal_detail, name='journal_detail'),
    path('journal/<str:journal_id>/delete/', views.journal_delete, name='journal_delete'),
    path('motivation/', views.motivation_list, name='motivation_list'),
    path('motivation/<str:motivation_id>/', views.motivation_detail, name='motivation_detail'),
]
