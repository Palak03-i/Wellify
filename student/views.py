"""
Student: chatbot (keyword-based), PHQ-9 assessment, book counselling session.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from accounts.models import User
from .stress_detector import detect_stress_level
from accounts.risk_engine import update_user_risk
from bson.objectid import ObjectId
import logging

from .models import ChatLog, Assessment, Appointment

logger = logging.getLogger(__name__)


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
    # determine current stress level for wellness tools and alerts
    stress = getattr(request.user, 'current_stress_level', 'Low') or 'Low'
    context = {
        'user': request.user,
        'stress': stress,
    }
    return render(request, 'student/student_dashboard.html', context)


@login_required
@require_POST
def chatbot_send(request):
    """Handle chatbot message: compute stress, save to MongoDB, return response."""
    if getattr(request.user, 'role', None) != 'Student':
        return JsonResponse({'error': 'Forbidden'}, status=403)
    msg = (request.POST.get('message') or '').strip()
    if not msg:
        return JsonResponse({'response': 'Please type a message.', 'stress_level': 'Low'})

    try:
        stress = detect_stress_level(msg)
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
            logger.warning(f'High-risk user detected: {request.user.id} - {request.user.email}')
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
    except Exception as e:
        logger.error(f'Error in chatbot_send: {str(e)}')
        return JsonResponse({
            'response': 'Sorry, something went wrong. Please try again.',
            'stress_level': 'Low',
            'error': True
        }, status=500)


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
        
        # Validate date format
        from datetime import datetime
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj.date() < datetime.now().date():
                messages.error(request, 'Please select a future date.')
                return render(request, 'student/book_session.html')
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return render(request, 'student/book_session.html')
        
        # Need at least one counsellor for appointment
        counsellor = User.objects.filter(role='Counsellor').first()
        if not counsellor:
            messages.error(request, 'No counsellor available. Please try later.')
            return render(request, 'student/book_session.html')
        
        try:
            Appointment(
                student_id=request.user.id,
                counsellor_id=counsellor.id,
                date=date,
                status='Pending'
            ).save()
            messages.success(request, 'Appointment requested. Counsellor will confirm.')
        except Exception as e:
            logger.error(f'Error booking appointment: {str(e)}')
            messages.error(request, 'Failed to book appointment. Please try again.')
        return redirect('student:student_dashboard')
    return render(request, 'student/book_session.html')


# ============ WELLNESS CONTENT VIEWS ============

@login_required
def meditation_list(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import MeditationGuide
    meditations = list(MeditationGuide.objects.order_by('-created_at'))
    return render(request, 'student/meditation_list.html', {'meditations': meditations})


@login_required
def meditation_detail(request, meditation_id):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import MeditationGuide
    try:
        meditation = MeditationGuide.objects.get(id=ObjectId(meditation_id))
    except (MeditationGuide.DoesNotExist, Exception) as e:
        logger.error(f'Error fetching meditation: {str(e)}')
        messages.error(request, 'Meditation not found.')
        return redirect('student:meditation_list')
    return render(request, 'student/meditation_detail.html', {'meditation': meditation})


@login_required
def breathing_list(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import BreathingExercise
    exercises = list(BreathingExercise.objects.order_by('-created_at'))
    return render(request, 'student/breathing_list.html', {'exercises': exercises})


@login_required
def breathing_detail(request, breathing_id):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import BreathingExercise
    try:
        exercise = BreathingExercise.objects.get(id=ObjectId(breathing_id))
    except (BreathingExercise.DoesNotExist, Exception) as e:
        logger.error(f'Error fetching breathing exercise: {str(e)}')
        messages.error(request, 'Exercise not found.')
        return redirect('student:breathing_list')
    return render(request, 'student/breathing_detail.html', {'exercise': exercise})


@login_required
def journal_list(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import JournalEntry
    entries = list(JournalEntry.objects.filter(user_id=request.user.id).order_by('-created_at'))
    return render(request, 'student/journal_list.html', {'entries': entries})


@login_required
def journal_create(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    if request.method == 'POST':
        from .models import JournalEntry
        content = (request.POST.get('content') or '').strip()
        mood = (request.POST.get('mood') or '').strip()
        stress = getattr(request.user, 'current_stress_level', 'Low') or 'Low'
        if not content:
            messages.error(request, 'Please write something in your journal.')
            return redirect('student:journal_create')
        JournalEntry(
            user_id=request.user.id,
            content=content,
            mood=mood,
            stress_level=stress,
        ).save()
        messages.success(request, 'Journal entry saved!')
        return redirect('student:journal_list')
    return render(request, 'student/journal_create.html')


@login_required
def journal_detail(request, journal_id):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import JournalEntry
    try:
        entry = JournalEntry.objects.get(id=ObjectId(journal_id), user_id=request.user.id)
    except (JournalEntry.DoesNotExist, Exception) as e:
        logger.error(f'Error fetching journal entry: {str(e)}')
        messages.error(request, 'Entry not found.')
        return redirect('student:journal_list')
    return render(request, 'student/journal_detail.html', {'entry': entry})


@login_required
def journal_delete(request, journal_id):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    if request.method != 'POST':
        return redirect('student:journal_list')
    from .models import JournalEntry
    try:
        entry = JournalEntry.objects.get(id=ObjectId(journal_id), user_id=request.user.id)
        entry.delete()
        messages.success(request, 'Journal entry deleted.')
    except (JournalEntry.DoesNotExist, Exception) as e:
        logger.error(f'Error deleting journal entry: {str(e)}')
        messages.error(request, 'Entry not found.')
    return redirect('student:journal_list')


@login_required
def motivation_list(request):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import MotivationalContent
    content = list(MotivationalContent.objects.order_by('-created_at'))
    return render(request, 'student/motivation_list.html', {'content': content})


@login_required
def motivation_detail(request, motivation_id):
    if getattr(request.user, 'role', None) != 'Student':
        return redirect('accounts:login')
    from .models import MotivationalContent
    try:
        item = MotivationalContent.objects.get(id=ObjectId(motivation_id))
    except (MotivationalContent.DoesNotExist, Exception) as e:
        logger.error(f'Error fetching motivational content: {str(e)}')
        messages.error(request, 'Content not found.')
        return redirect('student:motivation_list')
    return render(request, 'student/motivation_detail.html', {'item': item})

