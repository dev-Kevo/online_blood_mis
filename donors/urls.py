from django.urls import path
from . import views

urlpatterns = [
    path('', views.donors_dashboard, name='donor_dashboard'),
    path('profile/<int:pk>/', views.profile, name='donor_profile'),
    path('update_info/', views.donor_update_info, name='donor_update_info'),
    path('appointments/', views.appointments, name='appointments'),
    path('reports/', views.donor_report, name='donor_reports'),
    path('settings/', views.donor_settings, name='donor_settings'),
]
