"""
MongoEngine models stored in MongoDB: ChatLog, Assessment, Appointment.
user_id / student_id / counsellor_id refer to Django User id (integer).
"""
from mongoengine import Document, IntField, StringField, DateTimeField, FloatField
from datetime import datetime


class ChatLog(Document):
    user_id = IntField(required=True)
    message = StringField(required=True)
    response = StringField(required=True)
    stress_level = StringField(required=True)  # 'Low', 'Medium', 'High'
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'chat_logs'}


class Assessment(Document):
    user_id = IntField(required=True)
    total_score = IntField(required=True)  # legacy; use phq_score + gad_score
    stress_level = StringField(required=True)  # legacy; use final_level
    date = DateTimeField(default=datetime.utcnow)
    # Risk engine extension
    phq_score = IntField(default=0)
    gad_score = IntField(default=0)
    chat_stress_level = StringField(default='')
    final_level = StringField(default='')  # 'Low', 'Medium', 'High'
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'assessments'}


class Appointment(Document):
    student_id = IntField(required=True)
    counsellor_id = IntField(required=True)
    date = StringField(required=True)  # e.g. "2024-02-20"
    status = StringField(required=True, default='Pending')  # Pending, Approved, Completed

    meta = {'collection': 'appointments'}
