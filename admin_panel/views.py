"""
Admin: total users, total high-risk students, total appointments, delete user (basic CRUD).
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from student.models import ChatLog, Assessment, Appointment


@login_required
def admin_dashboard(request):
    if getattr(request.user, 'role', None) != 'Admin':
        messages.warning(request, 'Access denied.')
        return redirect('accounts:login')

    total_users = User.objects.count()
    high_risk_ids = set()
    for a in Assessment.objects.filter(stress_level='High'):
        high_risk_ids.add(a.user_id)
    for log in ChatLog.objects.filter(stress_level='High'):
        high_risk_ids.add(log.user_id)
    total_high_risk = len(high_risk_ids)
    total_appointments = Appointment.objects.count()
    users = User.objects.all().order_by('-date_joined')
 
    return render(request, 'admin_panel/admin_dashboard.html', {
        'total_users': total_users,
        'total_high_risk': total_high_risk,
        'total_appointments': total_appointments,
        'users': users,
    })


@login_required
def user_delete(request, user_id):
    if getattr(request.user, 'role', None) != 'Admin':
        return redirect('accounts:login')
    if request.method != 'POST':
        return redirect('admin_panel:admin_dashboard')

    target = User.objects.filter(id=user_id).first()
    if not target:
        messages.error(request, 'User not found.')
        return redirect('admin_panel:admin_dashboard')
    if target.id == request.user.id:
        messages.error(request, 'You cannot delete yourself.')
        return redirect('admin_panel:admin_dashboard')

    target.delete()
    messages.success(request, 'User deleted.')
    return redirect('admin_panel:admin_dashboard')
