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
#                    AFFIRMATION VIEWS 
# -------------------------------------------------------