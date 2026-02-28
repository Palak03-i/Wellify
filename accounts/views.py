from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm


def login_view(request):
    """Login view with role-based redirect."""
    if request.user.is_authenticated:
        return redirect('accounts:role_redirect')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                
                # Role-based redirect
                if user.role == "Student":
                    return redirect("accounts:student_dashboard")
                elif user.role == "Counsellor":
                    return redirect("accounts:counsellor_dashboard")
                elif user.role == "Admin":
                    return redirect("accounts:admin_dashboard")
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please provide both email and password.')

    return render(request, "login.html")


def register_view(request):
    """Register view with role-based redirect after registration."""
    if request.user.is_authenticated:
        return redirect('accounts:role_redirect')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.name}!')
            
            # Role-based redirect
            if user.role == "Student":
                return redirect("accounts:student_dashboard")
            elif user.role == "Counsellor":
                return redirect("accounts:counsellor_dashboard")
            elif user.role == "Admin":
                return redirect("accounts:admin_dashboard")
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {'form': form})


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def role_redirect_view(request):
    """Redirect user to their role-specific dashboard."""
    user = request.user
    if user.role == "Student":
        return redirect("accounts:student_dashboard")
    elif user.role == "Counsellor":
        return redirect("accounts:counsellor_dashboard")
    elif user.role == "Admin":
        return redirect("accounts:admin_dashboard")
    else:
        messages.warning(request, 'Invalid role. Please contact administrator.')
        return redirect('accounts:login')


@login_required
def student_dashboard(request):
    """Student dashboard view."""
    if request.user.role != "Student":
        messages.warning(request, 'Access denied. Student access only.')
        return redirect('accounts:login')
    return render(request, "student_dashboard.html", {'user': request.user})


@login_required
def counsellor_dashboard(request):
    """Counsellor dashboard view."""
    if request.user.role != "Counsellor":
        messages.warning(request, 'Access denied. Counsellor access only.')
        return redirect('accounts:login')
    return render(request, "counsellor_dashboard.html", {'user': request.user})


@login_required
def admin_dashboard(request):
    """Admin dashboard view."""
    if request.user.role != "Admin":
        messages.warning(request, 'Access denied. Admin access only.')
        return redirect('accounts:login')
    return render(request, "admin_dashboard.html", {'user': request.user})
