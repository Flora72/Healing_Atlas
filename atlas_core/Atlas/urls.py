from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('crisis/', views.crisis_mode, name='crisis'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('mood-tracker/', views.mood_tracker, name='mood_tracker'),
    path('affirmations/', views.affirmations, name='affirmations'),
    path('mental-health/', views.mental_health, name='mental_health'),
    path('journal/', views.journal_view, name='journal'),
    path('journal_entries/', views.journal_entries_view, name='journal_entries'),
    path('resources/', views.resources_page, name='resources'),
    path('emotion-data/', views.test_chart, name='emotion_data'),
    path('emotion_chart/', views.emotion_chart, name='emotion_chart'),
    path('dashboard_greeting/', views.dashboard_greeting, name='dashboard_greeting'),
    path('substance_support/', views.substance_support, name='substance_support'),
    path('upgrade/', views.upgrade_prompt, name='upgrade_prompt'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('checkout/', views.paystack_checkout, name='paystack_checkout'),
    path('journal_entries/edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('journal_entries/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('premium_insights', views.premium_insights, name='premium_insights'),
    path('checkins/', views.view_checkins, name='checkins'),
    path('test_chart/', views.test_chart, name='test_chart'),
    path('logout/', views.logout_view, name='logout'), 
]
