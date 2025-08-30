from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('crisis/', views.crisis_mode, name='crisis'),
    path('mood-tracker/', views.mood_tracker, name='mood_tracker'),
    path('affirmations/', views.affirmations, name='affirmations'),
    path('journal/', views.journal_space, name='journal'),
    path('resources/', views.resources_page, name='resources'),
    path('settings/', views.settings_page, name='settings'),
    path('admin/users/', views.manage_users, name='manage_users'),






]
