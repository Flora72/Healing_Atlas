from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Resource  
# -------------------------------------------------------
#                    GENERAL VIEWS 
# -------------------------------------------------------
def index(request):
    return render(request, 'index.html')


def crisis_mode(request):
    return render(request, 'crisis.html')


@login_required
def survivor_dashboard(request):
    return render(request, 'survivor_dashboard.html')

@login_required
def mental_health(request):
    return render(request, 'mental_health.html')

@login_required
def substance_support(request):
    return render(request, 'substance_support.html')

@login_required
def dashboard_greeting(request):
    return render(request, 'dashboard_greeting.html')

def logout_view(request):
    logout(request)
    return redirect('index')  

def resource_detail(request, id):
    resource = get_object_or_404(Resource, id=id)
    return render(request, 'resource_detail.html', {'resource': resource})

# -------------------------------------------------------
#                    AUTH VIEWS 
# -------------------------------------------------------
from .forms import CustomUserCreationForm
from django.contrib import messages


@login_required
def user_dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Role-based redirect
            role = getattr(user, 'role', None)
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'survivor':
                return redirect('dashboard')  
            else:
                return redirect('dashboard')  

        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')  
        else:
            print("Form errors:", form.errors) 
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# -------------------------------------------------------
#                    MOOD TRACKER VIEWS 
# -------------------------------------------------------
@login_required
def mood_tracker(request):
    return render(request, 'mood_tracker.html')


def mood_tracker_view(request):
    emotion_data = [
        {"date": "Aug 30", "score": 0.85, "sentiment": "hopeful"},
        {"date": "Aug 29", "score": 0.42, "sentiment": "tired"},
        {"date": "Aug 28", "score": 0.15, "sentiment": "anxious"},
    ]

    context = {
        "show_chart": True,
        "emotion_data": emotion_data,
        "emotion_data_json": json.dumps(emotion_data)
    }

    return render(request, "journal.html/dashboard_greeting/mood_tracker.html", context)



# -------------------------------------------------------
#                    AFFIRMATION VIEWS 
# -------------------------------------------------------
import random

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

@login_required
def resource_gallery(request):
    tone_filter = request.GET.get('tone')
    tag_filter = request.GET.get('tag')

    resources = Resource.objects.filter(is_archived=False)  # Start with only active ones

    if tone_filter:
        resources = resources.filter(emotional_tone=tone_filter)
    if tag_filter:
        resources = resources.filter(tags__name=tag_filter)

    tags = Tag.objects.all()
    return render(request, 'resource_gallery.html', {
        'resources': resources,
        'tags': tags,
        'selected_tag': tag_filter,
        'selected_tone': tone_filter,
    })


from .utils import suggest_tone

@login_required
def upload_resource(request):
    suggested_tone = None
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            suggested_tone = suggest_tone(resource.description)
            resource.emotional_tone = suggested_tone
            resource.save()
            return redirect('resources')
    else:
        form = ResourceForm()
    return render(request, 'upload_resource.html', {
        'form': form,
        'suggested_tone': suggested_tone
    })


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
#                    EDITING,DELETING RESOURCES VIEWS 
# -------------------------------------------------------
from django.shortcuts import get_object_or_404

@login_required
def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.emotional_tone = suggest_tone(updated.description)  # Optional re-check
            updated.save()
            form.save_m2m()
            return redirect('resources')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'edit_resource.html', {'form': form, 'resource': resource})

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        resource.is_archived = True
        resource.save()
        return redirect('resources')
    return render(request, 'confirm_delete.html', {'resource': resource})

@login_required
def restore_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.is_archived = False
    resource.save()
    return redirect('resources')


# -------------------------------------------------------
#                    JOURNAL/MOOD SCORE VIEWS 
# -------------------------------------------------------
import requests
import json
from django.views.decorators.csrf import csrf_exempt

def analyze_sentiment(entry_text):
    api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"}
    payload = {"inputs": entry_text}

    response = requests.post(api_url, headers=headers, json=payload)
    result = response.json()

    sentiment = result[0][0]['label']
    score = result[0][0]['score']
    return {"sentiment": sentiment, "score": score}

@csrf_exempt
def journal_view(request):
    emotion_data = []
    show_chart = False

    if request.method == "POST":
        mood = request.POST.get("mood")
        entry = request.POST.get("entry")

        # Analyze sentiment
        sentiment_result = analyze_sentiment(entry)
        emotion_data.append({
            "date": "Today",  
            "score": sentiment_result["score"],
            "sentiment": sentiment_result["sentiment"]
        })
        show_chart = True

    context = {
        "show_chart": show_chart,
        "emotion_data_json": json.dumps(emotion_data)
    }
    return render(request, "journal.html", context)

def dashboard_view(request):
    emotion_data = [
        {"date": "2025-08-30", "score": 0.85, "sentiment": "positive"},
        {"date": "2025-08-29", "score": 0.42, "sentiment": "neutral"},
        {"date": "2025-08-28", "score": 0.15, "sentiment": "low"},
    ]

    context = {
        "show_chart": True,
        "emotion_data_json": json.dumps(emotion_data)
    }

    return render(request, "your_template.html", context)

