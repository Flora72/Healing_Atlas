from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect,render
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import JournalEntry, MoodEntry
from .forms import MoodForm
import random,json
from django.utils.timezone import localtime
from .forms import JournalForm
from .utils import analyze_sentiment


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

# -------------------------------------------------------
#                    AUTH VIEWS 
# -------------------------------------------------------

@login_required
def user_dashboard(request):
    return render(request, 'dashboard_greeting.html')

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# -------------------------------------------------------
#                    MOOD TRACKER VIEWS 
# -------------------------------------------------------
def mood_tracker(request):
    form = MoodForm()

    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.score = 0.7  
            mood_entry.sentiment = "hopeful" 
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
def journal_view(request):
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        mood = request.POST.get('mood')
        entry = request.POST.get('entry')

        if mood and entry:
            sentiment_result = analyze_sentiment(entry)

            JournalEntry.objects.create(
                user=request.user,
                sentiment_label=mood,
                content=entry,
                sentiment_score=sentiment_result["score"]
            )
            messages.success(request, "Your journal entry has been saved. Your emotions have been gently reflected.")
            return redirect('/journal/')
        else:
            messages.error(request, "Please fill out both fields before submitting.")

    context = {
        'journal_entries': journal_entries
    }
    return render(request, "journal.html", context)

@login_required
def journal_entries_view(request):
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    emotion_data = [
        {
            "date": localtime(entry.created_at).strftime("%Y-%m-%d %H:%M"),
            "mood": entry.sentiment_label,
            "note": entry.content,
            "score": entry.sentiment_score
        }
        for entry in journal_entries
    ]

    context = {
        "journal_entries": journal_entries,
        "emotion_data": emotion_data
    }

    return render(request, "journal_entries.html", context)

# -------------------------------------------------------
#                    RESOURCES VIEWS 
# -------------------------------------------------------
@login_required
def resources_page(request):

    return render(request, 'resources.html')


# -------------------------------------------------------
#                    JOURNAL/MOOD SCORE VIEWS 
# -------------------------------------------------------
@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'username': user.username,
        'role': user.role,
        'membership': user.membership,
        'emotional_tone': user.emotional_tone,
        'safety_flag': user.safety_flag,
    }
    return render(request, 'dashboard.html', context)


@login_required
def test_chart(request):
    mood_entries = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')[:10]
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')[:10]

    mood_data = [
        {
            "date": localtime(entry.timestamp).strftime("%Y-%m-%d"),
            "score": entry.score,
            "sentiment": entry.sentiment
        }
        for entry in mood_entries if entry.score is not None
    ]

    journal_data = [
        {
            "date": localtime(entry.created_at).strftime("%Y-%m-%d"),
            "score": entry.sentiment_score,
            "sentiment": entry.sentiment_label
        }
        for entry in journal_entries if entry.sentiment_score is not None
    ]

    return JsonResponse({
        "mood_data": mood_data,
        "journal_data": journal_data
    })

 
@login_required
def emotion_chart(request):
    return render(request, 'emotion_chart.html')

def edit_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('journal_entries')
    else:
        form = JournalForm(instance=entry)
    return render(request, 'edit_entry.html', {'form': form, 'entry': entry})


def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('journal_entries')
    return render(request, 'confirm_delete.html', {'entry': entry})

@login_required
def view_checkins(request):
    checkins = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'view_checkins.html', {'checkins': checkins})

# -------------------------------------------------------
#                    PAYMENTS VIEWS 
# -------------------------------------------------------
@login_required
def verify_payment(request):
    reference = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['status'] and data['data']['status'] == 'success':
        amount = data['data']['amount'] 
        user = request.user

        # Assign membership tier based on amount
        if amount == 500:
            user.membership = 'basic'
        elif amount == 1500:
            user.membership = 'premium'
        user.save()

        return render(request, 'payment_success.html', {'tier': user.membership})
    else:
        return render(request, 'payment_failed.html')


def upgrade_prompt(request):
    return render(request, 'upgrade_prompt.html')


def paystack_checkout(request):
    tier = request.GET.get('tier', 'basic')
    context = {
        'tier': tier,
        'price': 'KES 500' if tier == 'basic' else 'KES 1200',
        'features': [
            'Emotion charts',
            'Journaling tools',
            'Mood tracking',
            'Resource library',
            'Priority support' if tier == 'premium' else 'Standard support'
        ]
    }

    return render(request, 'checkout.html', context)


def payment_confirmation(request):
    reference = request.GET.get('reference')
    tier = request.GET.get('tier', 'basic')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(url, headers=headers)
    result = response.json()

    if result['status'] and result['data']['status'] == 'success':
        # You can update user's subscription status here
        return render(request, 'payment_confirmation.html', {
            'tier': tier,
            'status': 'success',
            'amount': result['data']['amount'] / 100,  
            'reference': reference
        })
    else:
        return render(request, 'payment_confirmation.html', {
            'tier': tier,
            'status': 'failed',
            'reference': reference
        })
    
@login_required
@basic_required
def premium_insights(request):
    if not request.user.profile.is_premium:
        messages.warning(request, "This feature is available to premium members.")
        return redirect('dashboard')
    return render(request, 'premium_insights.html')



def initiate_payment(request):
    callback_url = request.build_absolute_uri(reverse('payment_confirmation'))
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": request.user.email,
        "amount": 5000 * 100,  
        "callback_url": callback_url
    }
    response = requests.post("https://api.paystack.co/transaction/initialize", 
                             headers=headers, json=data)
    res_data = response.json()
    return redirect(res_data['data']['authorization_url'])

