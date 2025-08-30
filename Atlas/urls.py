from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('crisis/', views.crisis_mode, name='crisis'),
    path('survivor/', views.survivor_dashboard, name='survivor_dashboard'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('mood-tracker/', views.mood_tracker, name='mood_tracker'),
    path('affirmations/', views.affirmations, name='affirmations'),
    path('mental-health/', views.mental_health, name='mental_health'),
    path('journal/', views.journal_space, name='journal'),
    path('resources/', views.resources_page, name='resources'),
    path('settings/', views.settings_page, name='settings'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/resources/', views.resource_gallery, name='resource_gallerry'),
    path('resource/<int:id>/', views.resource_detail, name='resource_detail'),
    path('admin/resources/edit/<int:resource_id>/', views.edit_resource, name='edit_resource'),
    path('admin/resources/delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    path('substance_support/', views.substance_support, name='substance_support'),
    path('logout/', views.logout_view, name='logout'), 

]
