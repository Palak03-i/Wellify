"""
Student: chatbot (keyword-based), PHQ-9 assessment, book counselling session.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from accounts.models import User
from accounts.risk_engine import update_user_risk

from .models import ChatLog, Assessment, Appointment


def _stress_from_message(text):
    """Keyword-based: suicide -> High; sad/anxiety -> Medium; else Low."""
    t = (text or '').strip().lower()
    if 'suicide' in t:
        return 'High'
    if any(w in t for w in ('sad', 'anxiety', 'anxious', 'depressed')):
        return 'Medium'
    return 'Low'


def _response_for_stress(level):
    if level == 'Low':
        return "That's good to hear. Keep taking care of yourself. You're doing great!"
    if level == 'Medium':
        return "It's okay to feel this way. Try: deep breathing, a short walk, or talking to someone you trust. You can also book a counselling session if you'd like extra support."
    # High
    return "We're concerned about your wellbeing. Please consider booking a counselling session as soon as you can. You're not alone – reach out to a counsellor or a trusted person."


@login_required
def student_dashboard(request):
    if getattr(request.user, 'role', None) != 'Student':
        messages.warning(request, 'Access denied.')
        return redirect('accounts:login')
    return render(request, 'student/student_dashboard.html', {'user': request.user})


@login_required
@require_POST
def chatbot_send(request):
    """Handle chatbot message: compute stress, save to MongoDB, return response."""
    if getattr(request.user, 'role', None) != 'Student':
        return JsonResponse({'error': 'Forbidden'}, status=403)
    msg = (request.POST.get('message') or '').strip()
    if not msg:
        return JsonResponse({'response': 'Please type a message.', 'stress_level': 'Low'})

    stress = _stress_from_message(msg)
    response_text = _response_for_stress(stress)

    ChatLog(
        user_id=request.user.id,
        message=msg,
        response=response_text,
        stress_level=stress
    ).save()

    # Risk engine: update user risk from chat
    final_level = update_user_risk(request.user, chat_level=stress)

    # Suggest assessment for Medium/High
    if stress in ('Medium', 'High'):
        response_text += ' We recommend completing a PHQ-9/GAD-7 assessment for better support.'
    if final_level == 'High':
        response_text += ' A counsellor has been notified and will reach out. You are not alone.'
        return JsonResponse({
            'response': response_text,
            'stress_level': stress,
            'show_alert': True,
            'counsellor_notified': True,
        })

    return JsonResponse({
        'response': response_text,
        'stress_level': stress,
        'show_alert': stress == 'High',
    })


def _get_phq_gad_from_request(request):
    """Parse PHQ-9 (q1..q9) and GAD-7 (g1..g7) from POST. Returns (phq_score, gad_score)."""
    phq = 0
    for i in range(1, 10):
        try:
            phq += int(request.POST.get(f'q{i}', 0))
        except ValueError:
            pass
    gad = 0
    for i in range(1, 8):
        try:
            gad += int(request.POST.get(f'g{i}', 0))
        except ValueError:
            pass
    return phq, gad


@login_required
def assessment_view(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    if request.method == 'POST':
        phq_score, gad_score = _get_phq_gad_from_request(request)
        from accounts.risk_engine import determine_final_level, update_user_risk
        final_level = determine_final_level(phq=phq_score, gad=gad_score)
        total_legacy = phq_score + gad_score  # for backward compatibility
        Assessment(
            user_id=request.user.id,
            total_score=total_legacy,
            stress_level=final_level,
            phq_score=phq_score,
            gad_score=gad_score,
            final_level=final_level,
        ).save()
        update_user_risk(request.user, phq=phq_score, gad=gad_score)
        request.session['assessment_result'] = {
            'phq_score': phq_score,
            'gad_score': gad_score,
            'final_level': final_level,
        }
        return redirect('student:assessment_result')
    return render(request, 'student/assessment.html')

@login_required
def chatbot_view(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    return render(request, 'student/chatbot.html')

@login_required
def assessment_result_view(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    data = request.session.pop('assessment_result', None)
    if not data:
        return redirect('student:assessment')
    return render(request, 'student/assessment_result.html', data)


@login_required
def book_session_view(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    if request.method == 'POST':
        date = (request.POST.get('date') or '').strip()
        if not date:
            messages.error(request, 'Please select a date.')
            return render(request, 'student/book_session.html')
        # Need at least one counsellor for appointment
        counsellor = User.objects.filter(role='Counsellor').first()
        if not counsellor:
            messages.error(request, 'No counsellor available. Please try later.')
            return render(request, 'student/book_session.html')
        Appointment(
            student_id=request.user.id,
            counsellor_id=counsellor.id,
            date=date,
            status='Pending'
        ).save()
        messages.success(request, 'Appointment requested. Counsellor will confirm.')
        return redirect('student:student_dashboard')
    return render(request, 'student/book_session.html')


