from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

# -------------------------------------------------------
#                    GENERAL VIEWS 
# -------------------------------------------------------
def landing(request):
    return render(request, 'landing.html')


def crisis_mode(request):
    return render(request, 'crisis.html')

# -------------------------------------------------------
#                    AUTH VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# -------------------------------------------------------
#                    MOOD TRACKER VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def mood_tracker(request):
    return render(request, 'mood_tracker.html')


# -------------------------------------------------------
#                    AFFIRMATION VIEWS 
# -------------------------------------------------------
import random
from django.contrib.auth.decorators import login_required

@login_required
def affirmations(request):
    affirmations_list = [
        "You are worthy of safety and care.",
        "Your story matters.",
        "Healing is not linear, and that’s okay.",
        "You are allowed to take up space.",
        "You are more than your survival — you are your strength.",
        "Gentleness is a form of power.",
        "You are not alone in this journey.",
        "Your pace is valid. Your path is yours."
    ]
    chosen_affirmation = random.choice(affirmations_list)
    return render(request, 'affirmations.html', {'affirmation': chosen_affirmation})

# -------------------------------------------------------
#                    JOURNAL VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def journal_space(request):
    return render(request, 'journal.html')


# -------------------------------------------------------
#                    RESOURCES VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def resources_page(request):
    return render(request, 'resources.html')


# -------------------------------------------------------
#                    SETTINGS VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required

@login_required
def settings_page(request):
    return render(request, 'settings.html')

# -------------------------------------------------------
#                  USER MANAGEMENT VIEWS 
# -------------------------------------------------------
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'manage_users.html', {'users': users})


# -------------------------------------------------------
#                    AFFIRMATION VIEWS 
# -------------------------------------------------------

# -------------------------------------------------------
#                    AFFIRMATION VIEWS 
# -------------------------------------------------------