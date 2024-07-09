from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients, name='patient_dashboard'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),
    path('update_info/', views.patient_update_info, name='patient_update_info'),
    path('profile/', views.profile, name='patient_profile'),
    path('reports/', views.reports, name='patient_reports'),
    path('settings/', views.settings, name='patient_settings'),
]