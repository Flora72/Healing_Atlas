from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Resource  
from django.http import JsonResponse


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
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import MoodEntry
from django.contrib import messages
from .forms import MoodForm


def mood_tracker(request):
    form = MoodForm()

    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.score = 0.7  # placeholder or calculated
            mood_entry.sentiment = "hopeful"  # placeholder or analyzed
            mood_entry.save()
            messages.success(request, "Your check-in has been saved. You’re doing beautifully.")
            return redirect('mood_tracker')

    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')[:10]
    emotion_data = [
        {
            "date": localtime(entry.timestamp).strftime("%Y-%m-%d"),
            "score": entry.score,
            "sentiment": entry.sentiment
        }
        for entry in mood_entries if entry.score is not None
    ]

    context = {
        "form": form,
        "emotion_data_json": json.dumps(emotion_data),
        "show_chart": True
    }

    return render(request, "mood_tracker.html", context)


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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import localtime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import JournalEntry
from textblob import TextBlob
import json

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Range: -1 to +1

    if polarity > 0.4:
        sentiment = "hopeful"
    elif polarity > 0.1:
        sentiment = "grateful"
    elif polarity < -0.3:
        sentiment = "anxious"
    elif polarity < -0.1:
        sentiment = "tired"
    else:
        sentiment = "calm"

    return {
        "score": round(polarity, 2),
        "sentiment": sentiment
    }

@login_required
@csrf_exempt
def journal_view(request):
    if request.method == "POST":
        mood = request.POST.get("mood")  # Optional, can be used for user reflection
        entry = request.POST.get("entry")

        if entry:
            sentiment_result = analyze_sentiment(entry)

            JournalEntry.objects.create(
                user=request.user,
                mood_label=sentiment_result["sentiment"],
                content=entry,
                sentiment_score=sentiment_result["score"]
            )

            messages.success(request, "Your journal entry has been saved. Thank you for sharing.")

            return redirect("journal")

    # Pull latest entries for chart
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by("created_at")
    emotion_data = [
        {
            "date": localtime(entry.created_at).strftime("%Y-%m-%d"),
            "score": entry.sentiment_score,
            "sentiment": entry.mood_label,
            "note": entry.content
        }
        for entry in journal_entries
    ]

    context = {
        "emotion_data_json": json.dumps(emotion_data),
        "show_chart": bool(emotion_data)
    }

    return render(request, "journal.html", context)

   

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
import json
from django.utils import timezone
from .utils import analyze_sentiment

@csrf_exempt
def journal_view(request):
    # Retrieve existing emotion data from session
    emotion_data = request.session.get("emotion_data", [])
    show_chart = bool(emotion_data)

    if request.method == "POST":
        mood = request.POST.get("mood")
        entry = request.POST.get("entry")

        if entry:
            # Analyze sentiment only if there's content
            sentiment_result = analyze_sentiment(entry)

            # Append new emotional data
            emotion_data.append({
                "date": timezone.now().strftime('%b %d'),  # e.g., "Aug 31"
                "score": sentiment_result["score"],
                "sentiment": sentiment_result["sentiment"],
                "mood": mood
            })

            # Save updated data to session
            request.session["emotion_data"] = emotion_data
            request.session.modified = True
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


import json
from django.utils.timezone import localtime
from .models import JournalEntry, MoodEntry

def test_chart(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')[:20]

    emotion_data = [
        {
            "date": localtime(entry.timestamp).strftime("%Y-%m-%d"),
            "score": entry.score,
            "sentiment": entry.sentiment,
            "note": entry.note or ""
        }
        for entry in entries
    ]

    context = {
        "emotion_data_json": json.dumps(emotion_data),
        "show_chart": True
    }

    return render(request, "test_chart.html", context)



    entries = MoodEntry.objects.filter(user=request.user).order_by('timestamp')
    emotion_data = [
        {
            "date": entry.timestamp.strftime("%Y-%m-%d"),
            "score": entry.score or 0,
            "sentiment": entry.sentiment or "neutral",
            "note": entry.note or ""
        }
        for entry in entries
    ]
    return render(request, 'test_chart.html', {
        'emotion_data_json': json.dumps(emotion_data)
    })

    user = request.user
    entries = MoodEntry.objects.filter(user=user).order_by('timestamp')

    emotion_data = [
        {
            "date": entry.timestamp.strftime("%Y-%m-%d"),
            "score": entry.score or 0,
            "sentiment": entry.sentiment or "neutral",
            "note": entry.note or ""
        }
        for entry in entries
    ]

    return render(request, 'emotional_chart.html', {
        'emotion_data_json': json.dumps(emotion_data)
    })

    emotion_data = [...]  # your queryset logic here
    context = {
        "emotion_data_json": json.dumps(emotion_data),
        "show_chart": True
    }
    return render(request, "test_chart.html", context)

    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')[:10]
    emotion_data = [
        {
            "date": localtime(entry.timestamp).strftime("%Y-%m-%d"),
            "score": entry.score,
            "sentiment": entry.sentiment
        }
        for entry in mood_entries if entry.score is not None
    ]
    return JsonResponse({"emotion_data": emotion_data})

    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('-created_at')

    combined_data = []

    for entry in journal_entries:
        combined_data.append({
            "date": localtime(entry.created_at).strftime("%Y-%m-%d"),
            "score": entry.sentiment_score,  # assuming you store this
            "sentiment": entry.sentiment_label  # e.g. "positive", "low"
        })

    for mood in mood_entries:
        combined_data.append({
            "date": localtime(mood.created_at).strftime("%Y-%m-%d"),
            "score": mood.mood_score / 100,  # normalize if needed
            "sentiment": mood.mood_label
        })

    # Optional: sort by date
    combined_data.sort(key=lambda x: x["date"])

    context = {
        "show_chart": True,
        "emotion_data_json": json.dumps(combined_data)
    }

    return render(request, "sentiment_chart.html", context)

    emotion_data = [
        {"date": "2025-08-30", "score": 0.85, "sentiment": "positive"},
        {"date": "2025-08-29", "score": 0.42, "sentiment": "neutral"},
        {"date": "2025-08-28", "score": 0.15, "sentiment": "low"},
    ]

    context = {
        "show_chart": True,
        "emotion_data_json": json.dumps(emotion_data)
    }

    return render(request, "test_chart.html", context)